# 🧑‍💻 Projeto de Reconhecimento Facial (IoT & IoB)

## 🎯 Objetivo
Este projeto implementa uma aplicação **local** (desktop/notebook) para **detecção e identificação facial** usando **OpenCV** e **face_recognition**.  
O sistema reconhece rostos em tempo real via webcam comparando-os com imagens de referência armazenadas em uma pasta.

---

## ⚙️ Tecnologias Utilizadas
- [Python 3.12](https://www.python.org/)
- [OpenCV](https://opencv.org/)
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [NumPy](https://numpy.org/)

---

## 📂 Estrutura do Projeto

```
Sprint3-IoT/
├── .idea/
├── referencias/
│   └── JoaoVieira.jpg               # Foto para a referencia de rosto conhecido
├── main.py                   
├── README.md                    
└── Sprint3_Iot ‐ Feito com o Clipchamp.MP4
```

---

## 🚀 Como Executar
1. Clone este repositório:
   ```bash
   git clone https://github.com/JBVJoaoV/Sprint3-IoT.git

2. Acesse o repositório:
   ````bash
   cd projeto-reconhecimento-facial
   
3. Instale as dependências:
   ````bash
   pip install opencv-python face_recognition numpy

4. Adicione imagens de referência na pasta `referencias/`
 
  - Use nomes de arquivos repretando a pessoa (ex.: **Joao.jpg**)

5. Execute o código:
  ````bash
  python reconhecimento.py
  ````

6. Precione **"q"** para encerrar a aplicação.

---

## 🔧 Parâmetros Relevantes

- `tolerance=0.6` → Define o nível de similaridade aceito (menor = mais rigoroso).
- Redimensionamento `fx=0.25, fy0.25` → Acelera processamento em tempo real.

---

## 📹 Demonstração

Segue abaixo o link do vídeo explicativo, caso haja algum problema em acessar, o mesmo se encontra na raiz do projeto.

[Vídeo explicativo](https://drive.google.com/file/d/1LHjaw35CsMCHOsdAPWHBmZPNgyQTnSMx/view?usp=sharing)

---

## 📌 Limitações

- Depende da qualidade das imagens de referência.
- Pode falhar devido a iluminação ou ângulos.
- Funciona localmente.
- Só aceita imagens do tipo **.jpg**.

---

## ⏩ Proximos passos

- Aprimorar o código para que receba mais arquivos de imagem além do `.jpg`.
- Conectar com um banco de dados para o armazenamento das fotos das pessoas conhecidas.

---

## 🔒 Nota Ética
Este projeto é apenas educacional. Dados faciais são sensíveis e devem ser tratados com **cuidado, privacidade e consentimento**.Não utilize este código em sistemas de vigilância ou coleta de dados sem autorização explícita.
