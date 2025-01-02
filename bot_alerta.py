
'''
PROJETO: Robô Alerta_NF
VERSÃO: 1.00
FINALIDADE: Automação de processos
AUTOR: Diego Cunha
CRIAÇÃO: Nov/2024

SITUAÇÃO/PROBLEMA:
No dia a dia da organização, o setor de faturamento utiliza uma API para sincronizar as notas fiscais emitidas com o site da prefeitura, evitando a necessidade de lançar manualmente tais informações.
O programa Alerta (AlertaExportaNotaFiscal.exe) deve permanecer em execuçáo fulltime, para garantir que não ocorram interrupções no processo de sincronia. Porém, é comum que ele pare de responder,
impactando o processo. Por ser uma etapa crucial para a atividade de faturamento, todas as vezes que o Alerta fica inativo, o setor de TI precisa acessar remotamente o servidor da aplicação, executar o 
Gerenciador de Tarefas, finalizar o processo do aplicativo e reiniciá-lo, e esse processo está consumindo muito tempo, pois o programa para de responder em média 10 vezes por dia.

SOLUÇÃO:
Visando a melhoria dos processos, foi criado um bot para otimizar e automatizar a execução do Alerta. Este robô monitora o status do aplicativo, verificando se ele está respondendo e, caso não esteja,
executa ações de fechamento, reabertura e limpeza de ícones fantasmas na tela, que ficam como "sujeira" após o fechamento da instância anterior do aplicativo. O robô também está configurado para abrir
a aplicação, caso detecte que ela não está em execução.

O bot é configurado para rodar continuamente, verificando o status do Alerta a cada 60 segundos, e gerando logs para monitorar o registro da atividade da aplicação.
Sua execução é feita através de um arquivo BAT, que fica sempre aberto no servidor.

DEPENDÊNCIAS:
Para sua execução, o código utiliza algumas bibliotecas que estão listadas a seguir:

+ subprocess: biblioteca utilizada para executar comandos do sistema operacional (fechar e abrir aplicativos) 
+ logging: biblioteca utilizada para configurar arquivos de log
+ time: biblioteca utitilizada para definir intervalos de pausa na execução do código
+ pyautogui: biblioteca utilizada para automação de movimentos do mouse
+ psutil: biblioteca utilizada para ler informações de desempenho do sistema (task manager)
'''

# IMPORTANDO BIBLIOTECAS
import subprocess
import logging
import time
import pyautogui
import psutil

# DEFININDO VARIÁVEIS DO APLICATIVO
app_name = "AlertaExportaNotaFiscal.exe"  # Nome completo do aplicativo a ser monitorado
app_path = "D:\\Piramide\\bin\\AlertaExportaNotaFiscal.exe"  # Caminho para o arquivo executável do aplicativo

# Configuração básica do logging para verificação da execução (incluindo data e hora de cada registro)
logging.basicConfig(
    level=logging.INFO, # Definindo log de nível INFO, para que todas as mensagens de nível crítico (WARNING, ERROR, CRITICAL) sejam registradas
    format='%(asctime)s - %(levelname)s - %(message)s', # Especifica o formato das mensagens de log. Aqui, o formato inclui: O timestamp da mensagem de log - O nível da mensagem de log - O conteúdo da mensagem de log
    datefmt='%d-%m-%Y %H:%M:%S', # Define o formato do timestamp. Neste caso, o formato é Dia-Mês-Ano Hora:Minuto:Segundo
    handlers=[
        logging.FileHandler("app_monitor.log"),
        logging.StreamHandler()
    ]
)

# DEFININDO FUNÇÃO PARA FECHAR O APP
def fechar_aplicativo():
    try:
        subprocess.run(["taskkill", "/IM", app_name, "/F"])
        logging.info(f"{app_name} fechado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao fechar {app_name}: {e}")

# DEFININDO FUNÇÃO PARA ABRIR O APP
def abrir_aplicativo():
    try:
        subprocess.Popen([app_path])
        logging.info(f"{app_name} aberto com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao abrir {app_name}: {e}")

# DEFININDO FUNÇÃO PARA LIMPAR OS ÍCONES QUE FICAM COM LIXO APÓS REINICIAR O APP
def limpar_ghost_icons():
    screen_width, screen_height = pyautogui.size() # Definindo o tamamho da tela de referência (abaixo, utilizamos os valores em porcentagem para que o código seja executado corretamente em qualquer tamanho de tela.)
    start_x = int(screen_width * 0.82)  # Iniciar o percurso do mouse a partir de 82% da largura da tela
    end_x = int(screen_width * 0.92)    # Finalizar o percurso do mouse em 92% da largura da tela
    y = screen_height - int(screen_height * 0.02)  # Nivelar o mouse em 2% da altura da tela a partir do fundo, para que o movimento horizontal atinja exatamente os ícones

    for x in range(start_x, end_x, int(screen_width * 0.01)):  # Percorrer o mouse à passos de 1% da largura da tela
        pyautogui.moveTo(x, y, duration=0.19) # Mover o mouse do ponto X ao ponto Y definidos acima (de 82% a 92% da tela)
        time.sleep(0.1)
    pyautogui.moveTo(screen_width // 2, screen_height // 2, duration=0.1) # Retornar o ponteiro do mouse para o meio da tela
    
# DEFININDO FUNÇÃO PRINCIPAL, PARA VERIFICAR O STATUS DO APLICATIVO
def verificar_status_aplicativo():
    try:
        for proc in psutil.process_iter(['name', 'cpu_percent']):
            if proc.info['name'] == app_name:
                cpu_usage = proc.cpu_percent(interval=30) # Verifica o uso de CPU durante um intervalo de 30 segundos, para evitar "falso travamento"
                if cpu_usage == 0: # Depois de 30 segundos com CPU = 0%, o código confirma que o processo está parado
                    logging.warning(f"{app_name} não está respondendo (uso de CPU = 0).") # Registra no arquivo de log o travamento do aplicativo
                    fechar_aplicativo() # Chama a função de fechamento
                    time.sleep(5)  # Aguarda 5 segundos antes de reabrir, para garantir que todos os processos vinculados à instância anterior do aplicativo sejam finalizados
                    abrir_aplicativo() # Chama a função de abertura
                    limpar_ghost_icons()  # Chama a função de limpeza dos ícones
                    return False # Retorna a condição FALSE para executar todas as funções
                logging.info(f"{app_name} está funcionando normalmente (uso de CPU = {cpu_usage}%).")
                return True # Confirma que o processo está rodando e lança no log a informação da linha anterior
        logging.warning(f"{app_name} não está em execução.") # Verifica que o programa NÃO ESTÁ EM EXECUÇÃO (diferente de estar travado)
        abrir_aplicativo() # Chama a função de abertura
        limpar_ghost_icons() # Chama a função de limpeza dos ícones
        return False # Retorna a condição FALSE para executar todas as funções
    except Exception as e:
        logging.error(f"Erro ao verificar status de {app_name}: {e}")
        return False

# Loop while para verificar continuamente o status do aplicativo
while True:
    if not verificar_status_aplicativo():
        pass
    time.sleep(60)  # Verifica o status do Alerta a cada 60 segundos e lança no log a informação de acordo com o status atual do aplicativo