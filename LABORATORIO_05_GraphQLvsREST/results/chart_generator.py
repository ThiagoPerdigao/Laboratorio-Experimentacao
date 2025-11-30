import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import os
import glob

print("🔍 Procurando arquivo measurements.csv...")

# Procurar o arquivo em todos os lugares possíveis
possible_locations = [
    'measurements.csv',                          # Na pasta atual
    '../measurements.csv',                       # Uma pasta acima
    '../../measurements.csv',                    # Duas pastas acima  
    '../results/measurements.csv',               # Pasta results um nível acima
    './results/measurements.csv',                # Pasta results na atual
    'LABORATORIO_05_GraphQLvsREST/results/measurements.csv',
    '../LABORATORIO_05_GraphQLvsREST/results/measurements.csv',
]

# Também procurar recursivamente
found_files = glob.glob('**/measurements.csv', recursive=True)

all_paths = possible_locations + found_files

csv_path = None
for path in all_paths:
    if os.path.exists(path):
        csv_path = path
        print(f"✅ Arquivo encontrado: {path}")
        break

if csv_path is None:
    print("❌ Arquivo measurements.csv não encontrado!")
    print("📁 Locais procurados:")
    for path in all_paths:
        print(f"   - {path}")
    print("\n💡 Solução: Coloque o measurements.csv na pasta results/ ou execute:")
    print("   python -c \"import os; print(os.getcwd())\"")
    exit(1)

# Agora carregar os dados
print(f"📊 Carregando dados de: {csv_path}")
df = pd.read_csv(csv_path)
print(f"✅ Dados carregados: {len(df)} linhas, {len(df.columns)} colunas")
print(f"🎯 Colunas: {list(df.columns)}")
print(f"📈 Amostra dos dados:")
print(df.head())

# Criar pasta para os gráficos se não existir
os.makedirs('results', exist_ok=True)

# Configurações de estilo
plt.style.use('default')
sns.set_palette("husl")
df['api_scenario'] = df['api'] + '_' + df['scenario']
order = ['REST_simple', 'GraphQL_simple', 'REST_complex', 'GraphQL_complex']

# 1. GRÁFICO TEMPORAL (mantido)
print("\n📊 Gerando Gráfico Temporal...")
plt.figure(figsize=(14, 8))
df_sorted = df.sort_values('timestamp').reset_index(drop=True)
df_sorted['execucao'] = range(len(df_sorted))
for api_scenario in order:
    subset = df_sorted[df_sorted['api_scenario'] == api_scenario]
    plt.plot(subset['execucao'], subset['duration_ms'], 
             marker='o', markersize=3, linewidth=1, label=api_scenario)
plt.title('Evolução dos Tempos de Resposta ao Longo das Execuções', fontsize=14, fontweight='bold')
plt.xlabel('Ordem de Execução')
plt.ylabel('Tempo (ms)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('results/1_grafico_temporal.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico temporal salvo!")

# 2. HEAT MAP DE PERFORMANCE
print("📊 Gerando Heat Map de Performance...")
# Criar matriz para o heatmap
heatmap_data = df.pivot_table(values='duration_ms', 
                             index='api', 
                             columns='scenario', 
                             aggfunc='mean')

plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, 
            annot=True, 
            fmt='.0f', 
            cmap='RdYlBu_r', 
            cbar_kws={'label': 'Tempo Médio (ms)'},
            linewidths=1,
            linecolor='white')
plt.title('Heat Map: Tempo Médio de Resposta por API e Cenário', fontsize=14, fontweight='bold')
plt.xlabel('Cenário')
plt.ylabel('API')
plt.tight_layout()
plt.savefig('results/2_heatmap_performance.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Heat Map de performance salvo!")

# 3. VIOLIN PLOTS COMBINADOS
print("📊 Gerando Violin Plots Combinados...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Violin plot para tempos
sns.violinplot(data=df, x='api_scenario', y='duration_ms', order=order, ax=ax1)
ax1.set_title('Distribuição dos Tempos de Resposta', fontweight='bold')
ax1.set_xlabel('API + Cenário')
ax1.set_ylabel('Tempo (ms)')
ax1.tick_params(axis='x', rotation=45)

# Violin plot para tamanhos
sns.violinplot(data=df, x='api_scenario', y='size_bytes', order=order, ax=ax2)
ax2.set_title('Distribuição dos Tamanhos de Resposta', fontweight='bold')
ax2.set_xlabel('API + Cenário')
ax2.set_ylabel('Tamanho (bytes)')
ax2.tick_params(axis='x', rotation=45)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))

plt.tight_layout()
plt.savefig('results/3_violin_plots_combinados.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Violin plots combinados salvos!")

# 4. SCATTER PLOT COM CORRELAÇÃO
print("📊 Gerando Scatter Plot com Correlação...")
plt.figure(figsize=(12, 8))

colors = {'REST': 'blue', 'GraphQL': 'red'}
markers = {'simple': 'o', 'complex': 's'}

for api in ['REST', 'GraphQL']:
    for scenario in ['simple', 'complex']:
        subset = df[(df['api'] == api) & (df['scenario'] == scenario)]
        
        # Calcular correlação
        correlation = subset['size_bytes'].corr(subset['duration_ms'])
        
        # Plotar pontos
        plt.scatter(subset['size_bytes'], subset['duration_ms'], 
                   c=colors[api], marker=markers[scenario], 
                   s=60, alpha=0.7, label=f'{api} {scenario} (r={correlation:.2f})')
        
        # Adicionar linha de tendência
        if len(subset) > 1:
            z = np.polyfit(subset['size_bytes'], subset['duration_ms'], 1)
            p = np.poly1d(z)
            plt.plot(subset['size_bytes'], p(subset['size_bytes']), 
                    color=colors[api], linestyle='--', alpha=0.5)

plt.title('Relação: Tempo vs Tamanho da Resposta (com Correlação)', fontsize=14, fontweight='bold')
plt.xlabel('Tamanho (bytes)')
plt.ylabel('Tempo (ms)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('results/4_scatter_correlacao.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Scatter plot com correlação salvo!")

# ESTATÍSTICAS RESUMO (mantido para referência)
print("📊 Gerando Estatísticas...")
estatisticas = df.groupby(['api', 'scenario']).agg({
    'duration_ms': ['count', 'mean', 'std', 'min', 'max'],
    'size_bytes': ['mean', 'std', 'min', 'max']
}).round(2)

print("\n" + "="*60)
print("📈 ESTATÍSTICAS RESUMO")
print("="*60)
print(estatisticas)

# Salvar estatísticas
with open('results/5_estatisticas.txt', 'w', encoding='utf-8') as f:
    f.write("ESTATÍSTICAS - EXPERIMENTO GraphQL vs REST\n")
    f.write("="*50 + "\n\n")
    f.write(str(estatisticas))

print("\n🎯 QUATRO GRÁFICOS PRINCIPAIS GERADOS COM SUCESSO!")
print("📁 Arquivos salvos na pasta 'results/':")
print("   1_grafico_temporal.png - Evolução temporal dos tempos")
print("   2_heatmap_performance.png - Mapa de calor da performance") 
print("   3_violin_plots_combinados.png - Distribuições completas")
print("   4_scatter_correlacao.png - Relação tempo×tamanho com correlação")
print("   5_estatisticas.txt - Estatísticas detalhadas")