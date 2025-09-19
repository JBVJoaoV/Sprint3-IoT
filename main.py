# Importando as bibliotecas
import cv2                      # OpenCV: leitura/recorte/exibição de imagens e vídeo (BGR por padrão).
import face_recognition         # Biblioteca que usa dlib para detectar rostos e gerar "encodings" faciais.
import numpy as np             # NumPy: operações numéricas; usado aqui para arrays e funções como argmin.
import os                      # Trabalhar com caminhos, diretórios e funções do sistema de arquivos.
import glob                    # Buscar arquivos por padrões (ex.: todos os *.jpg em uma pasta).


# Função para carregar encodings de referência
def carregar_referencias(diretorio_ref="referencias"):
    """
    Carrega imagens de referência de um diretório e gera encodings faciais.
    Retorna uma lista de nomes e outra com os encodings.
    """
    referencias_nomes = []  # Inicializa lista que irá conter os nomes (extraídos dos nomes dos arquivos).
    referencias_encodings = []  # Inicializa lista que irá conter os encodings (vetores numéricos).

    # Monta o caminho absoluto para o diretório de referências usando o diretório atual + nome fornecido.
    caminho_referencias = os.path.join(os.getcwd(), diretorio_ref)

    # Verifica se o diretório existe OU se existe ao menos um arquivo .jpg dentro dele.
    # Se qualquer uma das condições falhar, avisa e retorna listas vazias.
    # Nota: atualmente só checa arquivos "*.jpg" — outros formatos (png, jpeg) serão ignorados.
    if not os.path.exists(caminho_referencias) or not glob.glob(os.path.join(caminho_referencias, "*.jpg")):
        print(f"❌ O diretório '{diretorio_ref}' não existe ou não contém imagens.")
        return [], []  # Retorna listas vazias para evitar que o resto do programa quebre.

    # Percorre todos os arquivos .jpg no diretório de referências
    for arquivo_imagem in glob.glob(os.path.join(caminho_referencias, "*.jpg")):
        try:
            # Extrai o "nome" do arquivo sem sua extensão.
            # Ex.: "/caminho/Joao.jpg" -> basename = "Joao.jpg" -> splitext -> "Joao"
            nome = os.path.splitext(os.path.basename(arquivo_imagem))[0]

            # Carrega a imagem para memória como um array RGB (face_recognition espera array tipo numpy).
            imagem_referencia = face_recognition.load_image_file(arquivo_imagem)

            # Tenta extrair encodings faciais da imagem.
            # face_encodings retorna uma lista (um encoding por rosto detectado).
            encodings = face_recognition.face_encodings(imagem_referencia)

            if encodings:
                # Se foi encontrado pelo menos um rosto, pega o encoding e o adiciona.
                referencias_encodings.append(encodings[0])

                # Adiciona o nome correspondente ao mesmo índice que o encoding.
                referencias_nomes.append(nome)

                # Mensagem de sucesso para o usuário.
                print(f"✅ Rosto de '{nome}' carregado com sucesso.")
            else:
                # Se não houver rostos detectados na imagem, emite um aviso.
                print(f"⚠️ Aviso: Nenhum rosto encontrado na imagem '{arquivo_imagem}'.")

        except Exception as e:
            # Captura qualquer erro ao processar a imagem (arquivo corrompido, permissões, etc.)
            print(f"❌ Erro ao processar a imagem '{arquivo_imagem}': {e}")
            continue  # Continua para a próxima imagem mesmo se ocorrer erro com a atual.

    # Retorna duas listas: nomes (strings) e encodings (arrays numéricos)
    return referencias_nomes, referencias_encodings


# --- 1) Carrega todas as fotos de referência do diretório ---
nomes_conhecidos, encodings_conhecidos = carregar_referencias()
# Chama a função acima com o diretório padrão "referencias" e armazena resultados em duas variáveis.

# Se não encontrou nenhum encoding válido, avisa o usuário e encerra o programa.
# Sem encodings conhecidos, o reconhecimento não faria sentido.
if not encodings_conhecidos:
    print(
        "❌ Nenhum rosto de referência válido encontrado. Certifique-se de que há imagens de rosto na pasta 'referencias'.")
    exit()  # Finaliza a execução do script imediatamente.


# --- 2) Inicia webcam ---
cap = cv2.VideoCapture(0)  # Abre a câmera padrão (índice 0). Pode falhar se não houver câmera ou estiver ocupada.

print("\n▶️ Iniciando a detecção facial em tempo real. Pressione 'q' para sair.")

# Loop principal: captura frames continuamente até o usuário sair ou ocorrer erro
while True:
    ret, frame = cap.read()  # Lê um frame da webcam. 'ret' é bool indicando sucesso, 'frame' é a imagem.
    if not ret:
        # Se não conseguiu ler o frame (câmera desconectada, erro), mostra aviso e sai do loop.
        print("❌ Não foi possível ler o frame da webcam.")
        break

    # Redimensiona o frame para 25% do tamanho (fx=0.25, fy=0.25) para acelerar o processamento.
    # Isso reduz custo computacional (menos pixels para detectar/encodar).
    frame_pequeno = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Converte o frame de BGR (formato padrão do OpenCV) para RGB (formato esperado pelo face_recognition).
    rgb_frame = cv2.cvtColor(frame_pequeno, cv2.COLOR_BGR2RGB)

    # Detecta as posições (locations) de todos os rostos no frame reduzido.
    # Cada localização é uma tupla (top, right, bottom, left).
    localizacoes_rostos = face_recognition.face_locations(rgb_frame)

    # Calcula os encodings (vetores de características) para cada rosto detectado, usando as localizações.
    # Passar as localizações acelera o processo (evita nova detecção interna).
    encodings_rostos = face_recognition.face_encodings(rgb_frame, localizacoes_rostos)

    # Itera sobre cada rosto encontrado: localizacao e encoding correspondentes (zip).
    for (top, right, bottom, left), encoding_rosto in zip(localizacoes_rostos, encodings_rostos):
        nome_reconhecido = "Desconhecido"  # Valor padrão se não houver match.

        # Compara este encoding do frame com todos os encodings conhecidos.
        # Retorna uma lista de booleanos: True onde a distância está abaixo do 'tolerance'.
        # tolerance=0.6 é um valor comum (menor = mais rigoroso, maior = mais permissivo).
        comparacoes = face_recognition.compare_faces(encodings_conhecidos, encoding_rosto, tolerance=2.6)

        # Calcula as distâncias (valores numéricos) entre o encoding detectado e cada encoding conhecido.
        # Distâncias menores indicam rostos mais semelhantes.
        distancias_rostos = face_recognition.face_distance(encodings_conhecidos, encoding_rosto)

        # Encontra o índice do menor valor em 'distancias_rostos' -> melhor candidato (mais parecido).
        melhor_match_index = np.argmin(distancias_rostos)

        # Se o melhor candidato estiver marcado como True em 'comparacoes', então consideramos que é o mesmo rosto.
        # Observação: compare_faces pode retornar False para todos; por isso é importante checar o índice.
        if comparacoes[melhor_match_index]:
            # Se o candidato mais próximo for considerado um match, pega o nome correspondente.
            nome_reconhecido = nomes_conhecidos[melhor_match_index]
            cor = (0, 255, 0)  # Verde: rosto reconhecido
        else:
            # Se não for um match, mantém "Desconhecido" e pinta de vermelho.
            cor = (0, 0, 255)  # Vermelho: desconhecido

        # Ajusta as coordenadas do rosto para o tamanho original do frame.
        # Lembre-se: reduzimos a imagem em 0.25 (1/4), então ao desenhar precisamos multiplicar por 4.
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Desenha um retângulo (bounding box) ao redor do rosto no frame original.
        cv2.rectangle(frame, (left, top), (right, bottom), cor, 2)

        # Desenha um retângulo preenchido abaixo para servir de fundo ao texto (nome).
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), cor, cv2.FILLED)

        # Escreve o texto com o nome do reconhecido dentro do retângulo de fundo.
        # Parâmetros: imagem, texto, posição, fonte, escala, cor do texto (branco), espessura.
        cv2.putText(frame, nome_reconhecido, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.7,
                    (255, 255, 255), 1)

    # Exibe o frame (com retângulos e nomes) em uma janela chamada "Reconhecimento Facial em Tempo Real".
    cv2.imshow("Reconhecimento Facial em Tempo Real", frame)

    # Se a tecla 'q' for pressionada, sai do loop .
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera.
cap.release()

# Fecha todas as janelas criadas pelo OpenCV.
cv2.destroyAllWindows()
