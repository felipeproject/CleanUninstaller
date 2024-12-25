# CleanUninstaller

CleanUninstaller é uma ferramenta poderosa e de código aberto projetada para desinstalar programas do Windows completamente. Além de executar a desinstalação padrão, ela remove arquivos residuais e entradas no registro deixadas para trás, garantindo uma limpeza total do sistema.

## Características

- *Desinstalação Completa*:
  - Localiza e executa o desinstalador padrão do programa.
  - Remove arquivos, pastas e entradas no registro associados ao software.

- *Interface Simples*:
  - Fornece uma interface gráfica intuitiva para facilitar o uso.

- *Análise Avançada*:
  - Escaneia profundamente o sistema para encontrar todos os rastros deixados pelo programa desinstalado.

- *Portable*:
  - Funciona como um executável standalone, sem necessidade de instalação.

- *Código Aberto*:
  - Disponível para a comunidade, permitindo colaboração e melhorias.

## Tecnologias Utilizadas

- *Python*: Linguagem principal do projeto.
- *PyQt5* ou *Tkinter*: Para a interface gráfica.
- *pywin32*: Para interação com o registro do Windows.
- *PyInstaller*: Para criar o executável standalone.
- *unittest* e *Sphinx*: Para testes e documentação.

## Como Começar

### Clonando o Repositório
```bash
git clone https://github.com/seu-usuario/CleanUninstaller.git
cd CleanUninstaller
```

### Requisitos

Certifique-se de ter o Python 3.7 ou superior instalado. Em seguida, instale as dependências:
```bash
pip install -r requirements.txt
```

### Executando o Projeto

Para executar a aplicação:
```bash
python src/main.py
```

### Criando o Executável

Use o PyInstaller para gerar um executável portable:
```bash
pyinstaller --onefile src/main.py
```
O executável será gerado na pasta `dist/`.

## Contribuições

São bem-vindas contribuições da comunidade! Siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie um branch para suas modificações:
   ```bash
   git checkout -b minha-contribuicao
   ```
3. Faça o commit das alterações:
   ```bash
   git commit -m "Minha contribuição: explicando as melhorias"
   ```
4. Envie para o repositório remoto:
   ```bash
   git push origin minha-contribuicao
   ```
5. Abra um Pull Request no GitHub.



