
max_positive = 10
max_negative = -10

rgb_pos = (255,255,255)
rgb_neg = (255,255,255)
rgb_neu = (255,255,255)

positive_dif = (
    (rgb_pos[0] - rgb_neu[0]) / max_positive * 1.0, 
    (rgb_pos[1] - rgb_neu[1]) / max_positive * 1.0, 
    (rgb_pos[2] - rgb_neu[2]) / max_positive * 1.0
)

negative_dif = (
    (rgb_neu[0] - rgb_neg[0]) / max_negative * 1.0, 
    (rgb_neu[1] - rgb_neg[1]) / max_negative * 1.0, 
    (rgb_neu[2] - rgb_neg[2]) / max_negative * 1.0
)

round(rgb_neu[0] + value * positive_dif[0]) 
round(rgb_neu[1] + value * positive_dif[1]) 
round(rgb_neu[2] + value * positive_dif[2]) 

round(rgb_neu[0] + value * negative_dif[0]) 
round(rgb_neu[1] + value * negative_dif[1])
round(rgb_neu[2] + value * negative_dif[2]) 
