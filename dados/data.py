{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "bde8ba6e",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Dataset gerado com 5284 registros de 300 clientes.\n",
      "   id_agendamento  id_cliente nome_cliente     telefone data_atendimento  \\\n",
      "0               1           1  Cliente_001  98987423388       2025-11-26   \n",
      "1               2           1  Cliente_001  98987423388       2025-12-15   \n",
      "2               3           1  Cliente_001  98987423388       2026-01-01   \n",
      "3               4           1  Cliente_001  98987423388       2026-01-16   \n",
      "4               5           1  Cliente_001  98987423388       2026-01-29   \n",
      "\n",
      "  barbeiro        servico  valor_pago  \n",
      "0   Mateus          Corte        45.0  \n",
      "1    Lucas  Corte + Barba        75.0  \n",
      "2    Lucas          Corte        45.0  \n",
      "3    Lucas          Corte        45.0  \n",
      "4    Lucas          Corte        45.0  \n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "from datetime import datetime, timedelta\n",
    "\n",
    "np.random.seed(42)\n",
    "\n",
    "# Configurações da simulação\n",
    "n_clientes = 300\n",
    "data_inicio = datetime(2025, 11, 1)\n",
    "data_fim = datetime(2026, 11, 20)\n",
    "\n",
    "barbeiros = ['Lucas', 'Mateus', 'Rafael']\n",
    "servicos = {'Corte': 45.0, 'Corte + Barba': 75.0, 'Barba': 35.0, 'Sobrancelha': 15.0}\n",
    "\n",
    "registros = []\n",
    "\n",
    "for client_id in range(1, n_clientes + 1):\n",
    "    nome = f\"Cliente_{client_id:03d}\"\n",
    "    telefone = f\"9898{np.random.randint(1000000, 9999999)}\"\n",
    "    \n",
    "    # Variável interna oculta (não será salva no CSV final)\n",
    "    ciclo_oculto = np.random.choice([15, 21, 30, 45], p=[0.25, 0.40, 0.25, 0.10])\n",
    "    barbeiro_pref = np.random.choice(barbeiros)\n",
    "    \n",
    "    # Define se o cliente abandonou a barbearia (1) ou continua ativo (0)\n",
    "    deu_churn = np.random.choice([0, 1], p=[0.70, 0.30])\n",
    "    limite_data = data_fim - timedelta(days=np.random.randint(45, 120)) if deu_churn == 1 else data_fim\n",
    "    \n",
    "    data_atual = data_inicio + timedelta(days=np.random.randint(0, 30))\n",
    "    \n",
    "    while data_atual <= limite_data:\n",
    "        servico = np.random.choice(list(servicos.keys()), p=[0.50, 0.35, 0.10, 0.05])\n",
    "        valor = servicos[servico]\n",
    "        \n",
    "        # Adiciona variação natural de +/- 3 dias no retorno do cliente\n",
    "        intervalo_real = max(7, int(np.random.normal(ciclo_oculto, 3)))\n",
    "        \n",
    "        registros.append({\n",
    "            'id_agendamento': len(registros) + 1,\n",
    "            'id_cliente': client_id,\n",
    "            'nome_cliente': nome,\n",
    "            'telefone': telefone,\n",
    "            'data_atendimento': data_atual.strftime('%Y-%m-%d'),\n",
    "            'barbeiro': barbeiro_pref if np.random.rand() > 0.15 else np.random.choice(barbeiros),\n",
    "            'servico': servico,\n",
    "            'valor_pago': valor\n",
    "        })\n",
    "        \n",
    "        data_atual += timedelta(days=intervalo_real)\n",
    "\n",
    "df = pd.DataFrame(registros)\n",
    "df.to_csv('historico_barbearia.csv', index=False)\n",
    "print(f\"Dataset gerado com {len(df)} registros de {n_clientes} clientes.\")\n",
    "print(df.head())"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
