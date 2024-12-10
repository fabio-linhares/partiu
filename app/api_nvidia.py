from openai import OpenAI

def executar_api():
    try:
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key="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"
        )

        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[{"role": "user", "content": "Quem é você?"}],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=True
        )

        for chunk in completion:
            try:
                if chunk.choices[0].delta.content is not None:
                    print(chunk.choices[0].delta.content, end="")
            except Exception as e:
                print(f"Erro ao processar chunk: {str(e)}")
    
    except Exception as e:
        print(f"Erro ao executar a API: {str(e)}")

executar_api()