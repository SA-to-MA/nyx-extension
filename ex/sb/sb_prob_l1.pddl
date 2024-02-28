(define(problem angry_birds_prob)
(:domain angry_birds_scaled)
(:objects redbird_0 - bird hill_2 - platform hill_3 - platform hill_4 - platform hill_5 - platform hill_6 - platform hill_7 - platform hill_8 - platform hill_9 - platform hill_10 - platform hill_11 - platform hill_12 - platform hill_13 - platform hill_14 - platform hill_15 - platform hill_16 - platform hill_17 - platform hill_18 - platform hill_19 - platform hill_20 - platform hill_21 - platform hill_22 - platform hill_23 - platform hill_24 - platform hill_25 - platform hill_26 - platform hill_27 - platform pig_28 - pig dummy_block - block )
(:init 	(not (bird_released redbird_0) )
	(= (x_bird redbird_0)  192)
	(= (y_bird redbird_0)  28)
	(= (v_bird redbird_0)  270)
	(= (vx_bird redbird_0)  0)
	(= (vy_bird redbird_0)  0)
	(= (m_bird redbird_0)  1)
	(= (bounce_count redbird_0)  0)
	(= (bird_id redbird_0)  0)
	(= (x_platform hill_2)  526)
	(= (y_platform hill_2)  42.0)
	(= (platform_height hill_2)  17.0)
	(= (platform_width hill_2)  18.0)
	(= (x_platform hill_3)  526)
	(= (y_platform hill_3)  56.0)
	(= (platform_height hill_3)  17.0)
	(= (platform_width hill_3)  18.0)
	(= (x_platform hill_4)  526)
	(= (y_platform hill_4)  70.0)
	(= (platform_height hill_4)  17.0)
	(= (platform_width hill_4)  18.0)
	(= (x_platform hill_5)  526)
	(= (y_platform hill_5)  84.0)
	(= (platform_height hill_5)  17.0)
	(= (platform_width hill_5)  18.0)
	(= (x_platform hill_6)  526)
	(= (y_platform hill_6)  98.0)
	(= (platform_height hill_6)  17.0)
	(= (platform_width hill_6)  18.0)
	(= (x_platform hill_7)  526)
	(= (y_platform hill_7)  112.0)
	(= (platform_height hill_7)  17.0)
	(= (platform_width hill_7)  18.0)
	(= (x_platform hill_8)  526)
	(= (y_platform hill_8)  126.0)
	(= (platform_height hill_8)  17.0)
	(= (platform_width hill_8)  18.0)
	(= (x_platform hill_9)  526)
	(= (y_platform hill_9)  140.0)
	(= (platform_height hill_9)  17.0)
	(= (platform_width hill_9)  18.0)
	(= (x_platform hill_10)  526)
	(= (y_platform hill_10)  154.0)
	(= (platform_height hill_10)  17.0)
	(= (platform_width hill_10)  18.0)
	(= (x_platform hill_11)  526)
	(= (y_platform hill_11)  168.0)
	(= (platform_height hill_11)  17.0)
	(= (platform_width hill_11)  18.0)
	(= (x_platform hill_12)  526)
	(= (y_platform hill_12)  182.0)
	(= (platform_height hill_12)  17.0)
	(= (platform_width hill_12)  18.0)
	(= (x_platform hill_13)  526)
	(= (y_platform hill_13)  196.0)
	(= (platform_height hill_13)  17.0)
	(= (platform_width hill_13)  18.0)
	(= (x_platform hill_14)  526)
	(= (y_platform hill_14)  210.0)
	(= (platform_height hill_14)  17.0)
	(= (platform_width hill_14)  18.0)
	(= (x_platform hill_15)  540)
	(= (y_platform hill_15)  42.0)
	(= (platform_height hill_15)  17.0)
	(= (platform_width hill_15)  18.0)
	(= (x_platform hill_16)  540)
	(= (y_platform hill_16)  56.0)
	(= (platform_height hill_16)  17.0)
	(= (platform_width hill_16)  18.0)
	(= (x_platform hill_17)  540)
	(= (y_platform hill_17)  70.0)
	(= (platform_height hill_17)  17.0)
	(= (platform_width hill_17)  18.0)
	(= (x_platform hill_18)  540)
	(= (y_platform hill_18)  84.0)
	(= (platform_height hill_18)  17.0)
	(= (platform_width hill_18)  18.0)
	(= (x_platform hill_19)  540)
	(= (y_platform hill_19)  98.0)
	(= (platform_height hill_19)  17.0)
	(= (platform_width hill_19)  18.0)
	(= (x_platform hill_20)  540)
	(= (y_platform hill_20)  112.0)
	(= (platform_height hill_20)  17.0)
	(= (platform_width hill_20)  18.0)
	(= (x_platform hill_21)  540)
	(= (y_platform hill_21)  126.0)
	(= (platform_height hill_21)  17.0)
	(= (platform_width hill_21)  18.0)
	(= (x_platform hill_22)  540)
	(= (y_platform hill_22)  140.0)
	(= (platform_height hill_22)  17.0)
	(= (platform_width hill_22)  18.0)
	(= (x_platform hill_23)  540)
	(= (y_platform hill_23)  154.0)
	(= (platform_height hill_23)  17.0)
	(= (platform_width hill_23)  18.0)
	(= (x_platform hill_24)  540)
	(= (y_platform hill_24)  168.0)
	(= (platform_height hill_24)  17.0)
	(= (platform_width hill_24)  18.0)
	(= (x_platform hill_25)  540)
	(= (y_platform hill_25)  182.0)
	(= (platform_height hill_25)  17.0)
	(= (platform_width hill_25)  18.0)
	(= (x_platform hill_26)  540)
	(= (y_platform hill_26)  196.0)
	(= (platform_height hill_26)  17.0)
	(= (platform_width hill_26)  18.0)
	(= (x_platform hill_27)  540)
	(= (y_platform hill_27)  210.0)
	(= (platform_height hill_27)  17.0)
	(= (platform_width hill_27)  18.0)
	(not (pig_dead pig_28) )
	(= (x_pig pig_28)  602)
	(= (y_pig pig_28)  14.0)
	(= (pig_radius pig_28)  10)
	(= (m_pig pig_28)  1)
	(= (gravity)  134.2)
	(= (active_bird)  0)
	(= (angle)  0)
	(not (angle_adjusted) )
	(= (angle_rate)  10)
	(= (ground_damper)  0.4)
)
(:goal (and  (pig_dead pig_28) ))
(:metric minimize(total-time))
)
