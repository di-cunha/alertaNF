# alertaNF
Robô em Python que monitora a execução de um aplicativo e gerencia seu funcionamento de acordo com o status do processo no gerenciador de tarefas.

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
