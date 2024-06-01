# calculates CV coefficients of all charts in the same orders as they appear in paper figure

means = [
    [1.3, 2.3, 5.2, 10.2, 19.8, 45.7, 89.1],
    [1.0, 1.9, 5.0, 12.8, 25.3, 64.1, 138.6],
    [45.3, 77.4, 180.3, 351.1, 670.0, 1635.1, 3256.0]
]

devs = [
    [0.6, 1.3, 3.0, 5.8, 10.5, 26.1, 54.6],
    [0.3, 0.5, 1.6, 4.0, 6.9, 17.0, 27.6],
    [17.7, 50.5, 43.3, 66.1, 132.8, 338.5, 663.0]
]

cvs = []
for row, mean_list in enumerate(means):
    cvs.append([])
    for col, mean in enumerate(mean_list):
        cv = devs[row][col] / mean * 100
        cvs[row].append(cv)


for jakas_zmienna in cvs:
    sformatowana_podlista = [f"{cv:.1f}" for cv in jakas_zmienna]
    print(sformatowana_podlista)
