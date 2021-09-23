import random

l = [[1, 2], [2, 10], [10, 11], [11, 8], [8, 1], [1, 5], [2, 3], [9, 10], [20, 11], [7, 8], [5, 4],
                      [4, 3], [3, 12], [12, 9], [9, 19], [19, 20], [20, 17], [17, 7], [7, 6], [6, 5], [4, 14], [12, 13],
                      [18, 19], [16, 17], [15, 6], [14, 13], [13, 18], [18, 16], [16, 15], [15, 14]]

ll = [[0]*21 for _ in range(21)]

for i in l:
    ll[i[0]][i[1]] = 1
    ll[i[1]][i[0]] = 1
# print(ll)

# for i in ll:
# print(ll[1])
# for i in range(21):
    # if ll[1][i] == 1:
        # print(i)
for i in range(20):
    for j in range(1, 21):
        if ll[j][i] == 1:
            print(i,j)
# for i in ll[1]:
#     if ll[1][i] == 1:
#         print(i)
# print(ll)
