# ==========================================================
# Android Super Partition Space Checker
#
# Desenvolvido por: Guilherme Lima de Souza
# Matrícula: 85815
# Email: guilhermel@positivo.com.br
#
# Versão: 1.0

# Descrição:
# Ferramenta para análise de espaço da super partition
# utilizando dados do lpdump e cálculo baseado no SOP do ODM.
# ==========================================================

import subprocess
import os
import sys

# ANSI COLORS
ESC = "\033"
BLUE = f"{ESC}[94m"
CYAN = f"{ESC}[96m"
GREEN = f"{ESC}[92m"
RED = f"{ESC}[91m"
YELLOW = f"{ESC}[93m"
MAGENTA = f"{ESC}[95m"
RESET = f"{ESC}[0m"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode

print(f"{BLUE}============================================{RESET}")
print(f"{BLUE}  Android Super Partition Space Checker{RESET}")
print(f"{BLUE}============================================{RESET}\n")

# ADB check
_, code = run_cmd("adb version")
if code != 0:
    print(f"{RED}[ERRO] ADB nao encontrado.{RESET}")
    input()
    sys.exit()

# ETAPA 1
print(f"{CYAN}[1/4] Verificando dispositivo...{RESET}")
devices_output, _ = run_cmd("adb devices")

lines = devices_output.splitlines()[1:]
device = None

for line in lines:
    if line.strip() and "device" in line:
        device = line.split()[0]
        break

if not device:
    print(f"{RED}[ERRO] Nenhum dispositivo.{RESET}")
    input()
    sys.exit()

print(f"      {GREEN}{device}{RESET}\n")

# ETAPA 2
print(f"{CYAN}[2/4] Obtendo ID...{RESET}")
model, _ = run_cmd("adb shell getprop ro.product.model")
sw_version, _ = run_cmd("adb shell getprop ro.build.display.id")

display_id = model if model else f"device_{device}"
sw_version = sw_version if sw_version else "unknown"

print(f"      {GREEN}{display_id}{RESET}")
print(f"      {GREEN}{sw_version}{RESET}\n")

# ETAPA 3
print(f"{CYAN}[3/4] Executando lpdump...{RESET}")
lpdump, _ = run_cmd("adb shell lpdump")

print(f"{MAGENTA}================ LPDUMP ================={RESET}")
print(lpdump)
print(f"{MAGENTA}========================================={RESET}\n")

# ETAPA 4
print(f"{CYAN}[4/4] Entrada manual QA{RESET}")

try:
    last_sector = int(input("Ultimo sector do super: ").strip())
    total_bytes = int(input("Size total [block device table] (bytes): ").strip())
except:
    print(f"{RED}[ERRO] Entrada invalida{RESET}")
    input()
    sys.exit()

print(f"\n{YELLOW}>>> Calculando...{RESET}\n")

# CALCULO ODM
used_mb = (last_sector * 512) / (1000 * 1024)
total_mb = total_bytes / (1024 * 1024)
free_mb = total_mb - used_mb
free_gb = free_mb / 1024
total_gb = total_mb / 1024
used_gb = used_mb / 1024

# arredondar tudo
used_mb = round(used_mb, 2)
total_mb = round(total_mb, 2)
free_mb = round(free_mb, 2)
free_gb = round(free_gb, 2)
total_gb = round(total_gb, 2)
used_gb = round(used_gb, 2)

# RESULTADO
print(f"{BLUE}=============================================")
print(f"{BLUE}          RESULTADO FINAL{RESET}")
print(f"{BLUE}=============================================\n")

print(f"{CYAN}Dispositivo:{RESET} {display_id}")
print(f"{CYAN}Versao SW :{RESET} {sw_version}")

print()

print(f"{CYAN}Ultimo sector do super:{RESET} {last_sector}")
print(f"{CYAN}Total size:{RESET} {total_bytes} bytes")

print()

print(f"{CYAN}Total:{RESET} {GREEN}{total_mb:.2f} MB -> ({total_gb:.2f} GB){RESET}")
print(f"{CYAN}Usado:{RESET} {YELLOW}{used_mb:.2f} MB -> ({used_gb:.2f} GB){RESET}")
print(f"{CYAN}Livre:{RESET} {free_mb:.2f} MB -> ({free_gb:.2f} GB{RESET})")

print("\n=============================================")

# SALVAR
out_dir = os.path.join(os.getcwd(), "Outputs")
os.makedirs(out_dir, exist_ok=True)

safe_name = sw_version.replace(" ", "_")
outfile = os.path.join(out_dir, f"{safe_name}.txt")

with open(outfile, "w") as f:
    f.write("=============================================\n")
    f.write("               RESULTADO FINAL\n")
    f.write("=============================================\n\n")

    f.write(f"Dispositivo: {display_id}\n")
    f.write(f"Versao SW : {sw_version}\n\n")

    f.write(f"Ultimo sector do super: {last_sector}\n")
    f.write(f"Total size: {total_bytes} bytes\n\n")

    f.write(f"Total: {total_mb:.2f} MB -> ({total_gb:.2f} GB)\n")
    f.write(f"Usado: {used_mb:.2f} MB -> ({used_gb:.2f} GB)\n")
    f.write(f"Livre: {free_mb:.2f} MB -> ({free_gb:.2f} GB)\n")

    f.write("\n=============================================\n")

print(f"\n{GREEN}Salvo em:{RESET} {outfile}")

print(f"\n{GREEN}OK{RESET}")