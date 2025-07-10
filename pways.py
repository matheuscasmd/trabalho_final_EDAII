import sys
import os
import tempfile

class HeapMinima:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)
        self._sift_up(len(self.data) - 1)

    def pop(self):
        if not self.data:
            return None
        raiz = self.data[0]
        ultimo = self.data.pop()
        if self.data:
            self.data[0] = ultimo
            self._sift_down(0)
        return raiz

    def peek(self):
        if not self.data:
            return None
        return self.data[0]

    def _sift_up(self, idx):
        while idx > 0:
            pai = (idx - 1) // 2
            if self.data[idx][0] < self.data[pai][0]:
                self.data[idx], self.data[pai] = self.data[pai], self.data[idx]
                idx = pai
            else:
                break

    def _sift_down(self, idx):
        tamanho = len(self.data)
        while idx * 2 + 1 < tamanho:
            menor = idx
            esquerda = idx * 2 + 1
            direita = idx * 2 + 2

            if esquerda < tamanho and self.data[esquerda][0] < self.data[menor][0]:
                menor = esquerda
            if direita < tamanho and self.data[direita][0] < self.data[menor][0]:
                menor = direita

            if menor != idx:
                self.data[idx], self.data[menor] = self.data[menor], self.data[idx]
                idx = menor
            else:
                break

    def __len__(self):
        return len(self.data)

def substituicao(input_path, p):
    runs = []
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            conteudo_arquivo = f.read().strip()
            if not conteudo_arquivo:
                return []
            dados = list(map(int, conteudo_arquivo.split()))
    except FileNotFoundError:
        print(f"Erro: Arquivo de entrada não encontrado: {input_path}", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print(f"Erro: Conteúdo inválido no arquivo de entrada. Esperado inteiros: {input_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo de entrada {input_path}: {e}", file=sys.stderr)
        sys.exit(1)

    idx = 0
    n = len(dados)

    heap_substituicao = HeapMinima()
    for _ in range(p):
        if idx < n:
            heap_substituicao.push((dados[idx],))
            idx += 1
        else:
            break

    while len(heap_substituicao) > 0 or idx < n:
        elementos_run_atual = []
        proxima_run_heap = HeapMinima()
        valor_ultimo_removido = float('-inf')

        while len(heap_substituicao) > 0:
            valor_marcacao_minimo = heap_substituicao.pop()
            valor_minimo = valor_marcacao_minimo[0]

            if valor_minimo < valor_ultimo_removido:
                proxima_run_heap.push((valor_minimo,))
                continue

            elementos_run_atual.append(valor_minimo)
            valor_ultimo_removido = valor_minimo

            if idx < n:
                novo_valor = dados[idx]
                idx += 1

                if novo_valor >= valor_ultimo_removido:
                    heap_substituicao.push((novo_valor,))
                else:
                    proxima_run_heap.push((novo_valor,))

        if elementos_run_atual:
            try:
                arquivo_run = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
                for v in elementos_run_atual:
                    arquivo_run.write(f"{v}\n")
                arquivo_run.close()
                runs.append(arquivo_run.name)
            except Exception as e:
                print(f"Erro ao criar ou escrever arquivo temporário para run: {e}", file=sys.stderr)
                sys.exit(1)

        heap_substituicao = proxima_run_heap

        if len(heap_substituicao) == 0 and idx < n:
            for _ in range(p):
                if idx < n:
                    heap_substituicao.push((dados[idx],))
                    idx += 1
                else:
                    break

    return runs

def intercalar_runs(runs, p):
    total_passes = 0
    while len(runs) > 1:
        total_passes += 1
        nova_run_pass = []

        for i in range(0, len(runs), p):
            grupo_runs = runs[i:i + p]
            
            arquivos_para_tratamento_erro = [] 
            '''
            Para arquivos vazios, arquivos não existentes, arquivos que não tenham apenas inteiros, erro generalizado
            '''
            for caminho_arquivo in grupo_runs:
                try:
                    arquivos_para_tratamento_erro.append(open(caminho_arquivo, 'r', encoding='utf-8'))
                except FileNotFoundError:
                    print(f"Erro: Arquivo de run não encontrado: {caminho_arquivo}", file=sys.stderr)
                    for fh in arquivos_para_tratamento_erro: fh.close()
                    return None, total_passes
                except Exception as e:
                    print(f"Erro ao abrir arquivo de run {caminho_arquivo}: {e}", file=sys.stderr)
                    for fh in arquivos_para_tratamento_erro: fh.close()
                    return None, total_passes

            heap_merge = HeapMinima()
            
            for idx, handle_arquivo in enumerate(arquivos_para_tratamento_erro):
                line = handle_arquivo.readline()
                if line: # Adicionado: Verifica se a linha não está vazia
                    try:
                        heap_merge.push((int(line.strip()), idx))
                    except ValueError:
                        print(f"Erro ao ler linha de arquivo {grupo_runs[idx]}: {e}", file=sys.stderr)
                    except Exception as e:
                        print(f"Erro ao ler linha de arquivo {grupo_runs[idx]}: {e}", file=sys.stderr)

            run_merge_arquivos = None
            try:
                run_merge_arquivos = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')

                while len(heap_merge) > 0:
                    valor_minimo, idx_minimo = heap_merge.pop()
                    run_merge_arquivos.write(f"{valor_minimo}\n")

                    line = arquivos_para_tratamento_erro[idx_minimo].readline()
                    if line:
                        try:
                            heap_merge.push((int(line.strip()), idx_minimo))
                        except ValueError:
                            print(f"Erro ao ler linha de arquivo {grupo_runs[idx_minimo]}: {e}", file=sys.stderr)
                        except Exception as e:
                            print(f"Erro ao ler linha de arquivo {grupo_runs[idx_minimo]}: {e}", file=sys.stderr)
            except Exception as e:
                print(f"Ocorreu um erro durante a intercalção do grupo de runs: {e}", file=sys.stderr)
                if run_merge_arquivos: run_merge_arquivos.close(); os.remove(run_merge_arquivos.name)
                for fh in arquivos_para_tratamento_erro: fh.close()
                return None, total_passes
            finally:
                if run_merge_arquivos:
                    run_merge_arquivos.close()

            if run_merge_arquivos:
                nova_run_pass.append(run_merge_arquivos.name)

            for handle_arquivo in arquivos_para_tratamento_erro:
                handle_arquivo.close()
            for caminho_arquivo in grupo_runs:
                try:
                    os.remove(caminho_arquivo)
                except OSError as e:
                    print(f"Aviso: Não foi possível remover o arquivo temporário {caminho_arquivo}: {e}", file=sys.stderr)

        runs = nova_run_pass
    return runs[0] if runs else None, total_passes

def contar_registros(input_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            conteudo_arquivo = f.read().strip()
            if not conteudo_arquivo:
                return 0
            return len([s for s in conteudo_arquivo.split() if s])
    except FileNotFoundError:
        print(f"Erro: Arquivo de entrada não encontrado: {input_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo de entrada {input_path}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) != 4:
        print("Uso: pways <p> <input.txt> <output.txt>", file=sys.stderr)
        sys.exit(1)

    try:
        p = int(sys.argv[1])
    except ValueError:
        print("Erro: <p> deve ser um número inteiro.", file=sys.stderr)
        sys.exit(1)

    if p < 2:
        print("Erro: p deve ser >= 2.", file=sys.stderr)
        sys.exit(1)

    arquivo_entrada = sys.argv[2]
    arquivo_saida = sys.argv[3]

    total_registros = contar_registros(arquivo_entrada)

    if total_registros == 0:
        print("Arquivo de entrada vazio. Criando um arquivo de saída vazio.", file=sys.stderr)
        try:
            with open(arquivo_saida, 'w', encoding='utf-8') as f: pass
        except Exception as e:
            sys.exit(1)
        print(f"#Regs Ways #Runs #Parses")
        print(f"0 {p} 0 0")
        sys.exit(0)

    runs = substituicao(arquivo_entrada, p)

    if not runs:
        print("Nenhuma run gerada. O arquivo de entrada pode estar vazio ou um erro ocorreu.", file=sys.stderr)
        try:
            with open(arquivo_saida, 'w', encoding='utf-8') as f: pass
        except Exception as e:
            sys.exit(1)
        print(f"#Regs Ways #Runs #Parses")
        print(f"{total_registros} {p} 0 0")
        sys.exit(0)

    caminho_intercalar_runs, total_passes = intercalar_runs(runs, p)

    if caminho_intercalar_runs:
        try:
            os.rename(caminho_intercalar_runs, arquivo_saida)
        except OSError as e:
            sys.exit(1)
    else:
        sys.exit(1)

    print("#Regs Ways #Runs #Parses")
    print(f"{total_registros} {p} {len(runs)} {total_passes}")

if __name__ == "__main__":
    main()
''''''