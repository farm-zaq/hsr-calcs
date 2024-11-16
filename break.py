def calculate_break_damage(
  dmg_type, max_toughness,
  break_effect,
  def_shred,
  res, res_pen,
  vuln,
  reductions
):
  type_multipliers = {
    "physical": 2,
    "fire": 2,
    "ice": 1,
    "lightning": 1,
    "wind": 1.5,
    "quantum": 0.5,
    "imaginary": 0.5
  }
  toughness_multiplier = 0.5 + max_toughness / 40
  level_multiplier = 3767.5533
  base_dmg = type_multipliers[dmg_type] * toughness_multiplier * level_multiplier
  be_mult = 1 + break_effect / 100
  def_mult = (80.0 + 20.0) / ((95.0 + 20.0) * (1.0 - def_shred/100) + 80.0 + 20.0)
  res_mult = 1 - res / 100 + res_pen / 100
  vuln_mult = vuln_mult = 1 + vuln / 100
  reduction_mult = 1
  for reduction in reductions:
    reduction_mult = reduction_mult * (1 - reduction / 100)
  dmg = base_dmg * be_mult * def_mult * res_mult * vuln_mult * reduction_mult
  return dmg

def calculate_super_break_damage(
  toughness_reduction,
  super_multiplier,
  break_effect,
  def_shred,
  res, res_pen,
  vuln,
):
  level_multiplier = 3767.5533
  toughness_reduction_mult = toughness_reduction / 10
  be_mult = 1 + break_effect / 100
  def_mult = (80.0 + 20.0) / ((95.0 + 20.0) * (1.0 - def_shred/100) + 80.0 + 20.0)
  res_mult = 1 - res / 100 + res_pen / 100
  vuln_mult = 1 + vuln / 100
  dmg = level_multiplier * toughness_reduction_mult * super_multiplier * be_mult * def_mult * res_mult * vuln_mult
  return dmg

conservative_base_damage = calculate_break_damage("fire", 100, 481.3, 10, 0, 0, 24, [])
good_base_damage = calculate_break_damage("fire", 100, 481.3, 10, 0, 0, 34, [])
conservative_fugue_damage = calculate_break_damage("fire", 100, 481.3 + 30, 10 + 18, 0, 0, 24, [])
good_fugue_damage = calculate_break_damage("fire", 100, 481.3 + 30 + 12, 10 + 18 + 12, 0, 0, 24, [])

print(f"Conservative Fugue to Conservative FF: {100 * conservative_fugue_damage/conservative_base_damage - 100}")
print(f"Conservative Fugue to Good FF: {100 * conservative_fugue_damage/good_base_damage - 100}")
print(f"Good Fugue to Conservative FF: {100 * good_fugue_damage/conservative_base_damage - 100}")
print(f"Good Fugue to Good FF: {100 * good_fugue_damage/good_base_damage - 100}")

print()

conservative_base_damage = calculate_super_break_damage(30, 1.5, 481.3, 25, 0, 0, 24)
good_base_damage = calculate_super_break_damage(30, 1.5, 481.3, 25, 0, 0, 34)
conservative_fugue_damage = calculate_super_break_damage(30, 2.5, 481.3 + 30 + 6, 25 + 18, 0, 0, 24)
good_fugue_damage = calculate_super_break_damage(30, 2.5, 481.3 + 30 + 12, 25 + 18 + 12, 0, 0, 24)

print(f"Conservative Fugue to Conservative FF: {100 * conservative_fugue_damage/conservative_base_damage - 100}")
print(f"Conservative Fugue to Good FF: {100 * conservative_fugue_damage/good_base_damage - 100}")
print(f"Good Fugue to Conservative FF: {100 * good_fugue_damage/conservative_base_damage - 100}")
print(f"Good Fugue to Good FF: {100 * good_fugue_damage/good_base_damage - 100}")
