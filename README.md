# Ordenação Externa com p-Way Merge Sort

Implementação em Python do algoritmo de ordenação externa com:
- Geração de runs com **seleção por substituição** usando heap mínima com marcação
- Intercalação de p-caminhos (**p-way merge sort**) também com heap mínima implementada manualmente
- Compatível com grandes arquivos de entrada
- Sem uso de bibliotecas externas
---
## Passo a passo para execução

### 1. Clone o repositório

```bash
git clone https://github.com/matheuscasmd/trabalho_final_EDAII
cd trabalho_final_EDAII
```

### 2. Crie um ambiente virtual
Essa etapa é necessária para poder gerar o executável a partir do código, de acordo com o sistema operacional:
```bash
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate.bat     # Windows
```

### 3. Instale o pyinstaller

```bash
pip install pyinstaller
```

### 4. Gere o executável

```bash
pyinstaller --onefile pways.py
```

### 5. Execute o programa

Escolha o valor de p e passe como argumento:

```bash
./dist/pways <p> input.txt output.txt
```

**Exemplo:**
```bash
./dist/pways 3 input.txt output.txt
```

---

### 6. Formato de saída

```
#Regs Ways #Runs #Parses
25 3 5 2
```

### 7. Para sair

Apenas feche o terminal ou execute o comando:

```
deactivate
```


## Entrada 1 (input.txt)

O arquivo contém a sequência de exemplo contida na descrição do trabalho:
```txt
18 7 3 24 15 5 20 25 16 14 21 19 1 4 13 9 22 11 23 8 17 6 12 2 10
```

---

## Entrada 2 (input2.txt)

O arquivo contém a mesma sequência de 10000 inteiros fornecida pelo professor como caso de teste