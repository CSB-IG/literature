find . -name 'circos.png' -printf "convert %p -scale 1000x1000 %p_scaled.png\n" | sh
