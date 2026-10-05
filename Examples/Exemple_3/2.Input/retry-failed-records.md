[](</>)Docs & API

Search docs

⌘K

[Vibe](</vibe>)[Studio](</studio>)[Inference & Models](</inference>)[Admin](</admin>)[Resources](</resources>)[API Reference](</api>)

Search docs

⌘K

Toggle theme[Reach out](<https://mistral.ai/contact?utm_source=docs&utm_medium=header_cta&utm_campaign=studio_trial>)[Try Studio ](<https://console.mistral.ai?utm_source=docs&utm_medium=header_cta&utm_campaign=studio_trial>)

[Home](</>)

[Studio](</studio>)

  * [Overview](</studio>)
  * Build

  * Conversations

  * Agents

  * [Connectors](</studio/connectors>)

  * Workflows

  * Search

  * [Agentic Search](</studio/search/agentic-search>)
  * [Libraries](</studio/search/libraries>)

  * [Search Toolkit](</studio/search/search-toolkit>)

  * Process

  * Document AI

  * [Audio](</studio/audio/overview>)

  * [Batch Processing](</studio/batch-processing>)
  * Monitor

  * [Observability](</studio/observability>)

    * [Distributed tracing](</studio/observability/traces>)

    * [Offline evaluations](</studio/observability/evaluations>)

      * [Datasets](</studio/observability/evaluations/datasets>)
      * [System params](</studio/observability/evaluations/system-params>)
      * [Evaluators](</studio/observability/evaluations/evaluators>)
      * [Goals](</studio/observability/evaluations/goals>)
      * [Statistics](</studio/observability/evaluations/statistics>)
      * [Optimization](</studio/observability/evaluations/optimization>)

      * Advanced guides

        * [Use context objects](</studio/observability/evaluations/advanced-guides/context-objects>)
        * [Multiple evaluators](</studio/observability/evaluations/advanced-guides/multiple-evaluators>)
        * [Use run-level evaluators](</studio/observability/evaluations/advanced-guides/run-evaluators>)
        * [Iterate locally](</studio/observability/evaluations/advanced-guides/local-mode>)
        * [Reduce variance with multiple generations](</studio/observability/evaluations/advanced-guides/num-generations>)
        * [Retry failed records](</studio/observability/evaluations/advanced-guides/retry-failed-records>)
        * [Rescore persisted runs](</studio/observability/evaluations/advanced-guides/rescoring>)

      * [Workflows plugin](</studio/observability/evaluations/workflows-plugin>)

      * [API reference](</studio/observability/evaluations/api-reference>)

  * Safety & utilities

  * Embeddings

  * [Moderation & Guardrailing](</studio/safety-moderation>)
  * [Secrets Manager](</studio/secrets>)



  1. [](</>)
  2.   3. [Studio](</studio>)
  4.   5. [Observability](</studio/observability>)
  6.   7. [Offline evaluations](</studio/observability/evaluations>)
  8.   9. Advanced guides
  10.   11. Retry failed records



# Retry failed records

Evaluations can fail partially: a transient API error, a rate limit, or a bug in your scorer. Instead of rerunning the entire evaluation from scratch, the SDK lets you retry only the failed records and patch the results in place.

Why it matters

Copy section link

## Why it matters

A typical evaluation run can involve hundreds or thousands of LLM calls. If 5 out of 500 records fail, rerunning everything wastes time and money. `retry_failed_records()` identifies which records failed (at the generation or scoring level), reruns only those, and patches the original run so your results stay in one place in Studio.

Basic workflow

Copy section link

## Basic workflow
    
    
    import asyncio
    import os
    
    from mistralai.evaluations import (
        Evaluation, Evaluator, Mistral, ScorerContext, System, TaskContext,
    )
    
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    
    dataset = [
        {"prompt": "Say hello", "expected": "hello"},
        {"prompt": "Say goodbye", "expected": "goodbye"},
    ]
    
    async def task(ctx: TaskContext):
        response = await client.chat.complete_async(
            model=str(ctx.system.params["model"]),
            messages=[{"role": "user", "content": ctx.input_record["prompt"]}],
        )
        return str(response.choices[0].message.content)
    
    def scorer(ctx: ScorerContext):
        return 1 if ctx.input_record["expected"] in str(ctx.output).lower() else 0
    
    async def main():
        system = System(name="mistral-small", params={"model": "mistral-small-latest"})
    
        # Step 1: run the evaluation
        run = await client.evaluation.run(
            evaluation=Evaluation(name="My Eval"),
            system=system,
            dataset=dataset,
            task=task,
            evaluators=[Evaluator(name="accuracy", scorer=scorer)],
        )
    
        # Step 2: if some records failed, retry them
        result = await client.evaluation.retry_failed_records(
            run_id=run.run_id,
            dataset=dataset,
            task=task,
            evaluators=[Evaluator(name="accuracy", scorer=scorer)],
            system=system,
        )
        print(f"Retried: {result.retried_count}, Patched: {result.patched_count}")
    
    asyncio.run(main())
    
    
    import asyncio
    import os
    
    from mistralai.evaluations import (
        Evaluation, Evaluator, Mistral, ScorerContext, System, TaskContext,
    )
    
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    
    dataset = [
        {"prompt": "Say hello", "expected": "hello"},
        {"prompt": "Say goodbye", "expected": "goodbye"},
    ]
    
    async def task(ctx: TaskContext):
        response = await client.chat.complete_async(
            model=str(ctx.system.params["model"]),
            messages=[{"role": "user", "content": ctx.input_record["prompt"]}],
        )
        return str(response.choices[0].message.content)
    
    def scorer(ctx: ScorerContext):
        return 1 if ctx.input_record["expected"] in str(ctx.output).lower() else 0
    
    async def main():
        system = System(name="mistral-small", params={"model": "mistral-small-latest"})
    
        # Step 1: run the evaluation
        run = await client.evaluation.run(
            evaluation=Evaluation(name="My Eval"),
            system=system,
            dataset=dataset,
            task=task,
            evaluators=[Evaluator(name="accuracy", scorer=scorer)],
        )
    
        # Step 2: if some records failed, retry them
        result = await client.evaluation.retry_failed_records(
            run_id=run.run_id,
            dataset=dataset,
            task=task,
            evaluators=[Evaluator(name="accuracy", scorer=scorer)],
            system=system,
        )
        print(f"Retried: {result.retried_count}, Patched: {result.patched_count}")
    
    asyncio.run(main())

Fixing the task before retrying

Copy section link

## Fixing the task before retrying

You don't have to retry with the same task. If failures were caused by a bug in your code, fix it and pass the corrected version:
    
    
    # Fix the task, retry only the failed records
    async def fixed_task(ctx: TaskContext):
        response = await client.chat.complete_async(
            model=str(ctx.system.params["model"]),
            messages=[{"role": "user", "content": ctx.input_record["prompt"]}],
        )
        return str(response.choices[0].message.content)
    
    result = await client.evaluation.retry_failed_records(
        run_id=run.run_id,
        dataset=dataset,
        task=fixed_task,
        evaluators=[Evaluator(name="accuracy", scorer=scorer)],
        system=system,
    )
    
    
    # Fix the task, retry only the failed records
    async def fixed_task(ctx: TaskContext):
        response = await client.chat.complete_async(
            model=str(ctx.system.params["model"]),
            messages=[{"role": "user", "content": ctx.input_record["prompt"]}],
        )
        return str(response.choices[0].message.content)
    
    result = await client.evaluation.retry_failed_records(
        run_id=run.run_id,
        dataset=dataset,
        task=fixed_task,
        evaluators=[Evaluator(name="accuracy", scorer=scorer)],
        system=system,
    )

What happens

Copy section link

## What happens

  1. The SDK fetches the existing run and identifies records with status `"error"` (failed generation or scoring).
  2. Only those records are re-processed with the provided task and evaluators.
  3. Successful results are patched into the original run.
  4. If the original run had `run_evaluators`, their scores are recomputed with the updated data.



The original run in Studio is updated in place. No duplicate runs, no manual cleanup.

API reference

Copy section link

## API reference

`client.evaluation.retry_failed_records(...)` takes the following parameters:

Parameter| Type| Description  
---|---|---  
`run_id`| `str`| **Required.** ID of the run containing failed records.  
`dataset`| `Sequence[Mapping[str, Any]]`| **Required.** Same dataset used in the original run.  
`task`| `TaskFunction`| **Required.** Task function (can be a corrected version).  
`evaluators`| `list[Evaluator]`| **Required.** Evaluators to re-score with.  
`run_evaluators`| `list[RunEvaluator]`| Run-level evaluators to recompute after patching.  
`num_generations`| `int`| Number of generations per record (default: `1`).  
`system`| `System`| System params to inject into the task.  
`max_concurrency`| `int`| Maximum concurrent tasks (default: `10`).  
`upload_batch_size`| `int`| Batch size for uploading patched results (default: `10`).  
  
It returns a `RetryFailedRecordsResult`:

Field| Type| Description  
---|---|---  
`run_id`| `str`| ID of the run that was retried.  
`retried_count`| `int`| Number of records that were retried.  
`patched_count`| `int`| Number of records successfully patched.  
`run_scores_recomputed`| `bool`| Whether run-level scores were recomputed.  
  
### WHY MISTRAL

[About us](<https://mistral.ai/about>)[Our customers](<https://mistral.ai/customers>)[Careers](<https://mistral.ai/careers>)[Contact us](<https://mistral.ai/contact>)

### EXPLORE

[AI Solutions](<https://mistral.ai/solutions>)[Partners](<https://mistral.ai/partners>)[Research](<https://mistral.ai/news?category=Research>)

### DOCUMENTATION

[Documentation](</>)[Ambassadors](</resources/ambassadors>)[Cookbooks](</resources/cookbooks>)

### BUILD

[Studio](<https://console.mistral.ai>)[Vibe](<https://mistral.ai/products/vibe>)[Mistral Code](<https://mistral.ai/products/mistral-code>)[Mistral Compute](<https://mistral.ai/products/mistral-compute>)[Try the API](<https://docs.mistral.ai/api>)

### LEGAL

[Terms of service](<https://mistral.ai/terms>)[Privacy policy](<https://mistral.ai/terms#privacy-policy>)[Legal notice](<https://mistral.ai/legal>)Privacy Choices[Brand](<https://mistral.ai/brand>)

### COMMUNITY

[Discord↗](<https://discord.gg/mistralai>)[X↗](<https://x.com/mistralai>)[Github↗](<https://github.com/mistralai>)[LinkedIn↗](<https://linkedin.com/company/mistralai>)[Ambassadors](</resources/ambassadors>)

Mistral AI © 2026

Toggle theme

[Reduce variance with multiple generations](</studio/observability/evaluations/advanced-guides/num-generations>)[Rescore persisted runs](</studio/observability/evaluations/advanced-guides/rescoring>)