# PVP Agent Plugin Setup

This plugin uses a trained reinforcement learning model to play PVP in Last Man Standing.

## Integration Steps

1. The model files (`policy.pt` and `model_meta.json`) should be in the `resources/` directory
2. The implementation is in `src/pvp_agent.py`

## Required Customization

You will need to customize the following functions in the `pvp_agent.py` file:

- `get_observation()`: Extract game state from Microbot API to match the observations used in training
- `execute_action()`: Convert the model's action decisions to Microbot API calls

## Observation Mapping

The model expects these observations:

0. player_using_melee: Player using melee
1. player_using_ranged: Player using ranged
2. player_using_mage: Player using mage
3. player_spec_equipped: Player spec equipped
4. special_energy_percent: Special energy percent
5. player_melee_prayer: Player melee prayer
6. player_ranged_prayer: Player ranged prayer
7. player_magic_prayer: Player magic prayer
8. player_smite_prayer: Player smite prayer
9. player_redemption_prayer: Player redemption prayer
10. player_health_percent: Player's health percent
11. target_health_percent: Target's health percent
12. target_using_melee: Target using melee
13. target_using_ranged: Target using ranged
14. target_using_mage: Target using mage
15. target_spec_equipped: Target spec equipped
16. target_melee_prayer: Target melee prayer
17. target_ranged_prayer: Target ranged prayer
18. target_magic_prayer: Target magic prayer
19. target_smite_prayer: Target smite prayer
20. target_redemption_prayer: Target redemption prayer
21. target_special_percent: Target special percent
22. range_potion_doses: Range potion doses
23. combat_potion_doses: Combat potion doses
24. super_restore_doses: Super restore doses
25. brew_doses: Brew doses
26. food_count: Food count
27. karambwan_count: Karambwan count
28. prayer_points: Prayer points
29. player_frozen_ticks: Player's frozen ticks
30. target_frozen_ticks: Target's frozen ticks
31. player_frozen_immunity_ticks: Player's frozen immunity ticks
32. target_frozen_immunity_ticks: Target's frozen immunity ticks
33. player_location_can_melee: Player location can melee
34. strength_level: Strength level
35. attack_level: Attack level
36. defense_level: Defense level
37. ranged_level: Ranged level
38. magic_level: Magic level
39. attack_cycle_ticks: Attack cycle ticks
40. food_cycle_ticks: Food cycle ticks
41. potion_cycle_ticks: Potion cycle ticks
42. karambwan_cycle_ticks: Karambwan cycle ticks
43. food_attack_delay: Food attack delay
44. target_attack_cycle_ticks: Target attack cycle ticks
45. target_potion_cycle_ticks: Target potion cycle ticks
46. pending_damage_on_target: Pending damage on target
47. ticks_until_hit_on_target: Ticks until hit on target
48. ticks_until_hit_on_player: Ticks until hit on player
49. player_just_attacked: Player just attacked
50. target_just_attacked: Target just attacked
51. tick_new_attack_damage: Tick new attack damage
52. damage_on_player_tick: Damage on player tick
53. damage_on_target_tick: Damage on target tick
54. player_attacking_target: Player attacking target
55. player_is_moving: Player is moving
56. target_is_moving: Target is moving
57. player_has_pid: Player has PID
58. ice_barrage_usable: Ice barrage usable
59. blood_barrage_usable: Blood barrage usable
60. destination_to_target_distance: Destination to target distance
61. player_to_destination_distance: Player to destination distance
62. player_to_target_distance: Player to target distance
63. player_prayer_correct: Player prayer correct
64. target_prayer_correct: Target prayer correct
65. total_damage_dealt_scale: Total damage dealt scale (relative to damage received)
66. target_attack_confidence: Target attack confidence
67. target_melee_hit_percent: Target melee hit percent
68. target_magic_hit_percent: Target magic hit percent
69. target_ranged_hit_percent: Target ranged hit percent
70. player_melee_hit_percent: Player melee hit percent
71. player_magic_hit_percent: Player magic hit percent
72. player_ranged_hit_percent: Player ranged hit percent
73. target_number_of_hits_off_prayer: Target number of hits off prayer
74. target_prayer_confidence: Target prayer confidence
75. target_magic_prayer_percent: Target magic prayer percent
76. target_ranged_prayer_percent: Target ranged prayer percent
77. target_melee_prayer_percent: Target melee prayer percent
78. player_magic_prayer_percent: Player magic prayer percent
79. player_ranged_prayer_percent: Player ranged prayer percent
80. player_melee_prayer_percent: Player melee prayer percent
81. target_correct_pray_percent: Target correct pray percent
82. recent_target_melee_hit_percent: Recent (5) target melee hit percent
83. recent_target_magic_hit_percent: Recent (5) target magic hit percent
84. recent_target_ranged_hit_percent: Recent (5) target ranged hit percent
85. recent_player_melee_hit_percent: Recent (5) player melee hit percent
86. recent_player_magic_hit_percent: Recent (5) player magic hit percent
87. recent_player_ranged_hit_percent: Recent (5) player ranged hit percent
88. recent_target_number_of_hits_off_prayer: Recent (5) target number of hits off prayer
89. recent_target_magic_prayer_percent: Recent (5) target magic prayer percent
90. recent_target_ranged_prayer_percent: Recent (5) target ranged prayer percent
91. recent_target_melee_prayer_percent: Recent (5) target melee prayer percent
92. recent_player_magic_prayer_percent: Recent (5) player magic prayer percent
93. recent_player_ranged_prayer_percent: Recent (5) player ranged prayer percent
94. recent_player_melee_prayer_percent: Recent (5) player melee prayer percent
95. recent_target_correct_pray_percent: Recent (5) target correct pray percent
96. absolute_attack_level: Absolute attack level
97. absolute_strength_level: Absolute strength level
98. absolute_defense_level: Absolute defense level
99. absolute_ranged_level: Absolute ranged level
100. absolute_magic_level: Absolute magic level
101. absolute_prayer_level: Absolute prayer level
102. absolute_hitpoints_level: Absolute hitpoints level
103. is_enchanted_dragon_bolt: Is ranged using dragon bolts e
104. is_enchanted_opal_bolt: Is ranged using opal bolts e
105. is_enchanted_diamond_bolt: Is ranged using diamond bolts e
106. is_mage_spec_weapon_loadout: Is mage spec weapon in loadout
107. is_ranged_spec_weapon_loadout: Is ranged spec weapon in loadout
108. is_mage_spec_weapon_nightmare_staff: Is mage spec weapon volatile nightmare staff
109. is_ranged_spec_weapon_zaryte_cbow: Is ranged spec weapon zaryte cbow
110. is_ranged_spec_weapon_ballista: Is ranged spec weapon ballista
111. is_ranged_spec_weapon_morrigans_javelin: Is ranged spec weapon morrigan's javelins
112. is_ranged_spec_weapon_dragon_knife: Is ranged spec weapon dragon knife
113. is_ranged_spec_weapon_dark_bow: Is ranged spec weapon dark bow
114. is_melee_spec_dclaws: Is melee spec dragon claws
115. is_melee_spec_dds: Is melee spec dds
116. is_melee_spec_ags: Is melee spec ags
117. is_melee_spec_vls: Is melee spec vls
118. is_melee_spec_stat_hammer: Is melee spec stat hammer
119. is_melee_spec_ancient_godsword: Is melee spec ancient godsword
120. is_melee_spec_gmaul: Is melee spec granite maul
121. is_blood_fury: Is blood fury used for melee
122. is_dharoks_set: Is melee attacks using dharoks set
123. is_zuriel_staff: Is zuriel's staff used for magic
124. magic_accuracy: Expected magic accuracy
125. magic_strength: Expected magic strength
126. ranged_accuracy: Expected ranged accuracy
127. ranged_strength: Expected ranged strength
128. ranged_attack_speed: Expected ranged attack speed
129. ranged_attack_range: Expected ranged attack range
130. melee_accuracy: Expected melee accuracy
131. melee_strength: Expected melee strength
132. melee_attack_speed: Expected melee attack speed
133. magic_gear_ranged_defence: Magic gear ranged defence
134. magic_gear_mage_defence: Magic gear mage defence
135. magic_gear_melee_defence: Magic gear melee defence
136. ranged_gear_ranged_defence: Ranged gear ranged defence
137. ranged_gear_mage_defence: Ranged gear mage defence
138. ranged_gear_melee_defence: Ranged gear melee defence
139. melee_gear_ranged_defence: Melee gear ranged defence
140. melee_gear_mage_defence: Melee gear mage defence
141. melee_gear_melee_defence: Melee gear melee defence
142. target_current_gear_ranged_defence: Target current gear ranged defence
143. target_current_gear_mage_defence: Target current gear mage defence
144. target_current_gear_melee_defence: Target current gear melee defence
145. target_magic_accuracy: Expected target magic accuracy
146. target_magic_strength: Expected target magic strength
147. target_ranged_accuracy: Expected target ranged accuracy
148. target_ranged_strength: Expected target ranged strength
149. target_melee_accuracy: Expected target melee accuracy
150. target_melee_strength: Expected target melee strength
151. target_magic_gear_ranged_defence: Target magic gear ranged defence
152. target_magic_gear_mage_defence: Target magic gear mage defence
153. target_magic_gear_melee_defence: Target magic gear melee defence
154. target_ranged_gear_ranged_defence: Target ranged gear ranged defence
155. target_ranged_gear_mage_defence: Target ranged gear mage defence
156. target_ranged_gear_melee_defence: Target ranged gear melee defence
157. target_melee_gear_ranged_defence: Target melee gear ranged defence
158. target_melee_gear_mage_defence: Target melee gear mage defence
159. target_melee_gear_melee_defence: Target melee gear melee defence
160. is_lms_restrictions: Is fight using LMS restrictions
161. is_pvp_arena_rules: Is fight using PvP Arena rules (ex. no PID swap)
162. is_veng_active: Is player vengeance active
163. is_target_veng_active: Is target vengeance active
164. is_player_lunar_spellbook: Is player using lunar spellbook
165. is_target_lunar_spellbook: Is target using lunar spellbook
166. player_veng_cooldown_ticks: Ticks until player vengeance available
167. target_veng_cooldown_ticks: Ticks until target vengeance available
168. is_blood_magic_attack_available: Is blood magic attack available
169. is_ice_magic_attack_available: Is ice magic attack available
170. is_magic_spec_attack_available: Is magic spec attack available
171. is_range_attack_available: Is range attack available
172. is_range_spec_attack_available: Is range spec attack available
173. is_melee_attack_available: Is melee attack available
174. is_melee_spec_attack_available: Is melee spec attack available
175. is_food_anglerfish: Is primary food anglerfish (it can heal over max health)

## Action Mapping

The model can take these actions:

0. no_op_attack: No-op attack
1. mage_attack: Mage attack
2. ranged_attack: Ranged attack
3. melee_attack: Melee attack
4. no_melee_attack: No melee attack
5. basic_melee_attack: Basic melee attack
6. melee_special_attack: Melee special attack
7. no_ranged_attack: No ranged attack
8. basic_ranged_attack: Basic ranged attack
9. ranged_special_attack: Ranged special attack
10. no_mage_attack: No magic attack
11. use_ice_spell: Use ice spell
12. use_blood_spell: Use blood spell
13. use_magic_spec: Use magic spec
14. no_potion: No potion
15. use_brew: Use brew
16. use_restore_potion: Use restore potion
17. use_combat_potion: Use combat potion
18. use_ranged_potion: Use ranged potion
19. dont_eat_food: Don't eat food
20. eat_primary_food: Eat primary food
21. dont_karambwan: Don't karambwan
22. eat_karambwan: Eat karambwan
23. dont_use_veng: Don't use vengeance
24. use_veng: Use vengeance
25. no_gear: No gear swap
26. use_tank_gear: Use tank gear
27. dont_move: Don't move
28. move_next_to_target: Move next to target
29. move_under_target: Move under target
30. move_to_farcast_tile: Move to farcast tile
31. move_diagonal_to_target: Move diagonal to target
32. no_op_farcast: Don't move (farcast)
33. farcast_2_tiles: Farcast 2 tiles away
34. farcast_3_tiles: Farcast 3 tiles away
35. farcast_4_tiles: Farcast 4 tiles away
36. farcast_5_tiles: Farcast 5 tiles away
37. farcast_6_tiles: Farcast 6 tiles away
38. farcast_7_tiles: Farcast 7 tiles away
39. no_op_prayer: No-op prayer
40. mage_prayer: Mage prayer
41. ranged_prayer: Ranged prayer
42. melee_prayer: Melee prayer
43. smite_prayer: Smite prayer
44. redemption_prayer: Redemption prayer
