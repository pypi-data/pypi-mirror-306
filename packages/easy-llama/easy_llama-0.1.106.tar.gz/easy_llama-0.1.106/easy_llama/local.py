# local.py
# Python 3.12.3

import easy_llama as ez

system_prompt = \
"""You are an intelligent and helpful AI assistant."""

prompt_format = {
    "system_prefix": "",
    "system_prompt": system_prompt,
    "system_suffix": "",
    "user_prefix": "",
    "user_suffix": "",
    "bot_prefix": "",
    "bot_suffix": "",
    "stops": []
}

print("Loading model...")
Model = ez.Model(
    model_path='/Users/dylan/Documents/AI/models/',
    context_length=-1,
    n_gpu_layers=-1,
    offload_kqv=True,
    flash_attn=False,
    quantize_kv_cache=False,
    verbose=verbose
)

Thread = ez.Thread(
    model=Model,
    format=prompt_format,
    sampler=None,
    messages=None
)

print("Warming thread...")
Thread.warmup()

Thread.interact(
    color=not verbose,
    header='Header',
    stream=True,
    hook=None
)

print(repr(Thread))
print('-' * 32)
Thread.print_stats()
