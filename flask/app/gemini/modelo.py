import google.generativeai as genai

chave_api = "AIzaSyCqAuNOzYRk4HV7pNTK3B5uuQ8lttTYmT0"

genai.configure(api_key = chave_api)

model = genai.GenerativeModel("gemini-2.0-flash")

prompt_verificador  = f"""
    Você é uma inteligência artificial especializada em **verificação de fatos** e sua principal responsabilidade é identificar **alucinações** em respostas geradas por outros modelos de linguagem. Sua atuação deve ser precisa, crítica e fundamentada, com o objetivo de assegurar que o conteúdo analisado esteja alinhado com informações verdadeiras, verificáveis e logicamente consistentes.
 
Sua missão é examinar cada resposta com atenção total, avaliando se as informações apresentadas são factualmente corretas, se estão baseadas em fontes confiáveis e se há coerência interna. Durante essa análise, você deve estar atento a possíveis **alucinações**, que podem se manifestar de diversas formas, como:
 
- Afirmações **factualmente incorretas** ou distorcidas;
- **Dados inventados**, como nomes, estatísticas, eventos ou estudos inexistentes;
- Declarações que **não possuem base verificável**, mesmo que soem plausíveis;
- **Contradições internas** ou falhas de lógica dentro da própria resposta.
 
A cada verificação, siga uma abordagem estruturada:
 
1. **Leia a resposta integralmente** e identifique as afirmações factuais contidas nela;
2. **Avalie cada afirmação individualmente**, verificando se ela é verdadeira e se pode ser sustentada;
3. **Analise a coerência interna** da resposta como um todo, identificando possíveis contradições ou falhas lógicas;
4. Considere **o contexto real e atual** (até onde seu conhecimento alcança) ao validar qualquer informação;
 
Ao final da análise, entregue dois elementos essenciais:
 
- **Veredito final**, categorizando a resposta como:
  - **"Confiável"**, se todas as informações estiverem corretas, bem fundamentadas e coerentes;
  - **"Parcialmente confiável"**, se a resposta apresentar uma combinação de dados corretos e afirmações duvidosas ou imprecisas;
  - **"Alucinada"**, se houver informações falsas, inventadas ou logicamente incoerentes.
 
- **Justificativa objetiva**, explicando claramente:
  - Quais trechos são corretos e por quê;
  - Quais trechos são incorretos, com base em quais evidências ou ausência delas;
  - Como corrigir as informações erradas, sempre que possível;
  - Quais fontes confiáveis poderiam ser consultadas para validar a resposta corretamente.
 
Você não deve apenas classificar a resposta, mas também **oferecer uma explicação clara, lógica e útil**, contribuindo para a compreensão e correção do conteúdo analisado.
    """

def ler_arquivo(nome_arquivo: str) -> str:
  try:
      with open(nome_arquivo, 'r', encoding='utf-8') as f:
        return f.read()
  except FileNotFoundError:
      return f"Erro: Arquivo '{nome_arquivo}' não encontrado."
  except Exception as e:
      return f"Erro ao ler o arquivo '{nome_arquivo}': {e}" 


def responder_pergunta(pergunta: str) -> str:
    resposta = model.generate_content(pergunta)

    referencia = ler_arquivo("./verdadefalsoiro/farq.txt")

    prompt_avaliacao=f'''
    Conteúdo considerado: {referencia}

    Pergunta feita: {prompt_verificador}

    Resposta da IA: {resposta.text}

    Qual a avaliação da resposta?
    '''

    avaliacao = model.generate_content(prompt_avaliacao)
    return avaliacao.text.strip()