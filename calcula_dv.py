import re
import sys

def remove_caracteres(self, entrada):
    entrada_numerica =  re.sub("[-./]", "", entrada) # remove traço, ponto e barra
    return entrada_numerica

def calcula_cpf(ni):
    entrada_cpf = remove_caracteres(ni)
    if len(entrada_cpf) == 11 and entrada_cpf.isdecimal():
        cpf_calc = entrada_cpf[:9]
    elif len(entrada_cpf) == 9 and entrada_cpf.isdecimal():
        cpf_calc = entrada_cpf
    else:
        cpf_calc = None
        saida = f'Informe a entrada com 9 ou 11 \ndígitos'
        return saida
        sys.exit()

    if cpf_calc is not None:
        soma1 = 0
        for i in range(len(cpf_calc)):
            soma1 += int(cpf_calc[i]) * (10 - i)
        mod_11_1 = soma1 % 11
        if mod_11_1 < 2:
            dv1 = 0
        else:
            dv1 = 11 - mod_11_1
        cpf_dv1 = cpf_calc + str(dv1)
        soma2 = 0
        for j in range(len(cpf_dv1)):
            soma2 += int(cpf_dv1[j]) * (11 - j)
        mod_11_2 = soma2 % 11
        if mod_11_2 < 2:
            dv2 = 0
        else:
            dv2 = 11 - mod_11_2

        if len(entrada_cpf) == 9:
            saida = f'{entrada_cpf[:3]}.{entrada_cpf[3:6]}.{entrada_cpf[6:]} - DV = {str(dv1) + str(dv2)}'
        elif len(entrada_cpf) == 11 and entrada_cpf[-2:] == str(dv1) + str(dv2):
            saida = f'{entrada_cpf[:3]}.{entrada_cpf[3:6]}.{entrada_cpf[6:9]}-{entrada_cpf[-2:]} correto!'
        else:
            saida = f'{entrada_cpf[:3]}.{entrada_cpf[3:6]}.{entrada_cpf[6:9]}-{entrada_cpf[-2:]} incorreto!\nDV calculado = {str(dv1) + str(dv2)}'
        return saida

def calcula_cnpj(ni):
    entrada_cnpj = remove_caracteres(ni)
    if len(entrada_cnpj) == 14 and entrada_cnpj.isdecimal():
        cnpj_calc = entrada_cnpj[:12]
    elif len(entrada_cnpj) == 12 and entrada_cnpj.isdecimal():
        cnpj_calc = entrada_cnpj
    else:
        cnpj_calc = None
        saida = f'Informe a entrada com 14 ou 12 \ndígitos'
        return saida
        sys.exit()

    if cnpj_calc is not None:
        soma1 = 0
        for i in range(len(cnpj_calc)):
            if i < 4:
                soma1 += int(cnpj_calc[i]) * (5 - i)
            else:
                soma1 += int(cnpj_calc[i]) * (13 - i)
        mod_11_1 = soma1 % 11
        if mod_11_1 < 2:
            dv1 = 0
        else:
            dv1 = 11 - mod_11_1
        cnpj_dv1 = cnpj_calc + str(dv1)
        soma2 = 0
        for j in range(len(cnpj_dv1)):
            if j < 5:
                soma2 += int(cnpj_dv1[j]) * (6 - j)
            else:
                soma2 += int(cnpj_dv1[j]) * (14 - j)
        mod_11_2 = soma2 % 11
        if mod_11_2 < 2:
            dv2 = 0
        else:
            dv2 = 11 - mod_11_2
        if len(entrada_cnpj) == 12:
            saida = f'{entrada_cnpj[:2]}.{entrada_cnpj[2:5]}.{entrada_cnpj[5:8]}/{entrada_cnpj[8:]} - DV = {str(dv1) + str(dv2)}'
        elif len(entrada_cnpj) == 14 and entrada_cnpj[-2:] == str(dv1) + str(dv2):
            saida = f'{entrada_cnpj[:2]}.{entrada_cnpj[2:5]}.{entrada_cnpj[5:8]}/{entrada_cnpj[8:12]}-{entrada_cnpj[-2:]} correto!'
        else:
            saida = f'{entrada_cnpj[:2]}.{entrada_cnpj[2:5]}.{entrada_cnpj[5:8]}/{entrada_cnpj[8:12]}-{entrada_cnpj[-2:]} incorreto!\nDV calculado = {str(dv1) + str(dv2)}'
        return saida

def calcula_processo(processo, tipo):
    entrada_processo = self.remove_caracteres(proc)
    if (len(entrada_processo) == 17 and tipo == 1) or (len(entrada_processo) == 15 and tipo == 2) \
            and entrada_processo.isdecimal():
        proc_calc = entrada_processo[:-2]
    elif (len(entrada_processo) == 15 and tipo == 1) or \
            (len(entrada_processo) == 13 and tipo == 2) and entrada_processo.isdecimal():
        proc_calc = entrada_processo
    else:
        proc_calc = None
        if tipo == 1:
            saída = f'Informe a entrada com 17 ou \n15 dígitos'
        else:
            saida  = f'Informe a entrada com 15 ou \n13 dígitos'
        return saida
        exit.sys()

    if proc_calc is not None:
        soma1 = 0
        for i in range(len(proc_calc)):
                soma1 += int(proc_calc[i]) * (len(proc_calc) + 1 - i)
        mod_11_1 = soma1 % 11
        if mod_11_1 == 0:
            dv1 = 1
        elif mod_11_1 == 1:
            dv1 = 0
        else:
            dv1 = 11 - mod_11_1
        proc_dv1 = proc_calc + str(dv1)
        soma2 = 0
        for j in range(len(proc_dv1)):
            soma2 += int(proc_dv1[j]) * (len(proc_calc) + 2 - j)
        mod_11_2 = soma2 % 11
        if mod_11_2 == 0:
            dv2 = 1
        elif mod_11_2 == 1:
            dv2 = 0
        else:
            dv2 = 11 - mod_11_2

        if len(entrada_processo) == 13:
            saida = f'{entrada_processo[:5]}-{entrada_processo[5:8]}.{entrada_processo[8:11]}/{entrada_processo[-2:]} - DV = {str(dv1) + str(dv2)}'
        elif len(entrada_processo) == 15 and tipo == 1:
            saida = f'{entrada_processo[:5]}-{entrada_processo[5:8]}.{entrada_processo[8:11]}/{entrada_processo[-4:]} - DV = {str(dv1) + str(dv2)}'

        elif len(entrada_processo) == 15 and tipo == 2:
            if entrada_processo[-2:] == str(dv1) + str(dv2):
                saida = f'{entrada_processo[:5]}-{entrada_processo[5:8]}.{entrada_processo[8:11]}/{entrada_processo[11:13]}-{entrada_processo[-2:]} correto!'
            else:
                saida = f'{entrada_processo[:5]}-{entrada_processo[5:8]}.{entrada_processo[8:11]}/{entrada_processo[11:13]}-{entrada_processo[-2:]} \nincorreto! DV calculado = {str(dv1) + str(dv2)}'
        else:
            if entrada_processo[-2:] == str(dv1) + str(dv2):
                saida = f'{entrada_processo[:5]}-{entrada_processo[5:8]}.{entrada_processo[8:11]}/{entrada_processo[11:15]}-{entrada_processo[-2:]} correto!'
            else:
                saida = f'{entrada_processo[:5]}-{entrada_processo[5:8]}.{entrada_processo[8:11]}/{entrada_processo[11:15]}-{entrada_processo[-2:]} \nincorreto! DV calculado = {str(dv1) + str(dv2)}'
        return saida