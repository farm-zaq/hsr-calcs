char_cost = (45381074 / 745633) * .5823 + (45381074 / 745633) * 2 * (1 - .5823)
cone_cost = (15168296 / 302693) * .791 + (15168296 / 302693) * 2 * (1 - .791)

feixiao = {
  "base_atk": 1130, #1097, 1116
  "fua_scaling": 110,
  "fua_extra": 0,
  "skill_scaling": 200,
  "skill_extra": 0,
  "ult_scaling": 700,
  "ult_extra": 0,
  "extra_mult": 0,

  "atk": 3281,
  "scaling_attr": "atk",
  "crit_dmg": 102.4,
  "crit_rate": 91.8,
  "elemental_dmg_mult": 38.8,
  "all_type_dmg_mult": 0,
  "def_shred": 0,
  "res": 20,
  "res_pen": 0,
  "elemental_vuln": 0,
  "all_vuln": 0,
  "reductions": [10]
}

topaz = {
  "base_atk": 1097,
  "basic_scaling": 100,
  "basic_extra": 0,
  "fua_scaling": 150,
  "fua_extra": 0,
  "skill_scaling": 150,
  "skill_extra": 0,
  "extra_mult": 0,

  "atk": 2310,
  "scaling_attr": "atk",
  "crit_dmg": 121.9,
  "crit_rate": 76.9,
  "elemental_dmg_mult": 38.8 + 22.4,
  "all_type_dmg_mult": 0,
  "def_shred": 0,
  "res": 20,
  "res_pen": 0,
  "elemental_vuln": 0,
  "all_vuln": 0,
  "reductions": [10]
}

robin = {
  "base_atk": 1116,
  "ult_scaling": 120,
  "ult_extra": 0,
  "extra_mult": 0,

  "atk": 4060,
  "scaling_attr": "atk",
  "crit_dmg": 150,
  "crit_rate": 100,
  "elemental_dmg_mult": 0,
  "all_type_dmg_mult": 0,
  "def_shred": 0,
  "res": 20,
  "res_pen": 0,
  "elemental_vuln": 0,
  "all_vuln": 0,
  "reductions": [10]
}

aven = {
  "base_atk": 0,
  "base_defe": 1117,
  "fua_scaling": 175,
  "fua_extra": 0,
  "basic_scaling": 100,
  "basic_extra": 0,
  "ult_scaling": 270,
  "ult_extra": 0,
  "extra_mult": 0,

  "atk": 0,
  "defe": 3505,
  "scaling_attr": "defe",
  "crit_dmg": 141.3,
  "crit_rate": 37,
  "elemental_dmg_mult": 14.4,
  "all_type_dmg_mult": 0,
  "def_shred": 0,
  "res": 20,
  "res_pen": 0,
  "elemental_vuln": 0,
  "all_vuln": 0,
  "reductions": [10]
}

thunderhunt = {
  "all_type_dmg_mult": 60
}

#fua
formshift = {
  "crit_dmg": 36
}

boltcatch = {
  "atk_percent": 48
}

#ult
valorous = {
  "all_type_dmg_mult": 36
}

duran = {
  "crit_dmg": 25
}

#fua
duran_fua = {
  "all_type_dmg_mult": 25,
}

#fua
proof = {
  "all_vuln": 50,
}

swordplay = {
  "all_type_dmg_mult": 20
}

#fua
duke_2 = {
  "all_type_dmg_mult": 20
}

duke_4 = {
  "atk_percent": 24
}

aria = {
  "all_type_dmg_mult": 50
}

tonal = {
  "crit_dmg": 20
}

#fua
flourish = {
  "crit_dmg": 25
}

fleet = {
  "atk_percent": 8
}

journey = {
  "all_type_dmg_mult": 30
}

def leverage(defe):
  return {
    "crit_rate": min(((defe - 1600) // 100 * 2), 48)
  }

red_or_black = {
  "defe_percent": 60
}

concert = {
  "all_type_dmg_mult": 20
}

robin_atk = robin["atk"] + robin["base_atk"] * fleet["atk_percent"]/100
concerto = {
  "atk": .228 * robin_atk + 200
}

robin_buffs = {
  "base": [fleet],
  "ult": [journey],
  "concerto": [concerto]
}

feixiao_buffs = {
  "base": [thunderhunt, boltcatch, duran, aria, tonal, fleet],
  "fua": [formshift, duran_fua, proof],
  "concerto": [concerto],
  "concerto_fua": [flourish],
  "concerto_ult": [valorous] + [formshift, duran_fua, proof] + [flourish]
}

topaz_buffs = {
  "base": [duran, duran_fua, proof, swordplay, duke_2, duke_4, aria, tonal, fleet],
  "fua": [],
  "concerto": [concerto],
  "concerto_fua": [flourish],
  "concerto_basic": [flourish],
}

aven_buffs = {
  "base": [duran, aria, tonal, concert, leverage(aven["defe"])],
  "fua": [duran_fua, proof, duke_2],
  "concerto": [concerto],
  "concerto_fua": [flourish],
}

aven_first_buffs = {
  "base": [duran, aria, tonal, concert, leverage(aven["defe"] + 0.6 * aven["base_defe"]), red_or_black],
  "fua": [duran_fua, proof, duke_2],
  "concerto": [concerto],
  "concerto_fua": [flourish],
}

prisoners = {
  "crit_dmg": 20
}

feixiao_buffs["base"] += [prisoners]
topaz_buffs["base"] += [prisoners]
feixiao_buffs["base"] += [prisoners]
aven_buffs["base"] += [prisoners]

e1_aven_team = {
  "robin": robin,
  "robin_buffs": robin_buffs,
  "feixiao": feixiao,
  "feixiao_buffs": feixiao_buffs,
  "topaz": topaz,
  "topaz_buffs": topaz_buffs,
  "aven": aven,
  "aven_first_buffs": aven_first_buffs,
  "aven_buffs": aven_buffs,
  "cost": char_cost,
  "name": "e1 aven\t"
}