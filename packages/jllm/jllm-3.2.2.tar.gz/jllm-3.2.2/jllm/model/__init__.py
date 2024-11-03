from .llama.pipeline_llama import LlamaForCausalLMPipe,autopartition_transformer
from .baichuan.pipeline_baichuan import BaichuanForCausalLMPipe
from .qwen.pipeline_qwen import QWenForCausalLMPipe,QWenForClassCausalLMPipe
from .qwen2.pipeline_qwen2 import Qwen2ForCausalLMPipe
from .lora import convert_linear_layer_to_lora,_z3_params_to_fetch,convert_lora_to_linear_layer,only_optimize_lora_parameters,make_model_gradient_checkpointing_compatible
from .llama.parallel_llama import LlamaForCausalLMPipe as LlamaForCausalLMParallel
from .qwen2.parallel_qwen2 import Qwen2ForCausalLMPipe as Qwen2ForCausalLMParallel
from .qwen2.pipeline_qwen2_moe import Qwen2MoeForCausalLMPipe
from .qwen2_vl.pipeline_qwen2_vl import Qwen2VLForCausalLMPipe
from .intern.pipeline_internvl2 import InterenVL2ForCausalLMPipe,autopartition_decoder
from .intern.pipeline_internlm2 import InternLM2ForCausalLMPipe

ModelPipe = {
    'LlamaForCausalLM':LlamaForCausalLMPipe,
    'QWenLMHeadModel':QWenForCausalLMPipe,
    'Qwen2ForCausalLM':Qwen2ForCausalLMPipe,
    'QWenForClassCausalLM':QWenForClassCausalLMPipe,
    'BaichuanForCausalLM':BaichuanForCausalLMPipe,
    'Qwen2MoeForCausalLM':Qwen2MoeForCausalLMPipe,
    'InternVLChatModel':InterenVL2ForCausalLMPipe,
    'InternLM2ForCausalLM':InternLM2ForCausalLMPipe,
    'Qwen2VLForConditionalGeneration':Qwen2VLForCausalLMPipe
}
    
ModelParallel = {
    'LlamaForCausalLM':LlamaForCausalLMParallel,
    'Qwen2ForCausalLM':Qwen2ForCausalLMParallel
}