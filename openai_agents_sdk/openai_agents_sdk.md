

## ollama local LLM hosting

I found that the default context length of the gpt-oss is ohnly 8k in length.  These steps can expand it to the maximum length?

Create a "Modelfile" to define the model you want to create.

`
FROM <model-name>
PARAMETER num_ctx 131072
`

`
FROM gpt-oss:20b 
PARAMETER num_ctx 131072
`

now, create the new model:
ollama create gpt-oss_131k_context:20b -f ./Modelfile

```
gathering model components 
using existing layer sha256:e7b273f9636059a689e3ddcab3716e4f65abe0143ac978e46673ad0e52d09efb 
using existing layer sha256:fa6710a93d78da62641e192361344be7a8c0a1c3737f139cf89f20ce1626b99c 
using existing layer sha256:f60356777647e927149cbd4c0ec1314a90caba9400ad205ddc4ce47ed001c2d6 
creating new layer sha256:131728b247995ae3b23ca201f792cc11d2db047a92a8f3c23fcb59344f4dce7d 
writing manifest 
success 
```

Now, if I run `ollama list`, I see the new model:

```
NAME                        ID              SIZE      MODIFIED      
gpt-oss_131k_context:20b    4d2f07cece89    13 GB     2 minutes ago    
gpt-oss:20b                 17052f91a42e    13 GB     13 hours ago     
llama3.2:latest             a80c4f17acd5    2.0 GB    8 weeks ago      
qwen2.5-coder:1.5b-base     02e0f2817a89    986 MB    6 months ago     
llama3.1:8b                 46e0c10c039e    4.9 GB    6 months ago     
codellama:latest            8fdf8f752f6e    3.8 GB    6 months ago     
nomic-embed-text:latest     0a109f422b47    274 MB    7 months ago 
```

