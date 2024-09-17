from encryptionProject.image_recognition.functions_and_constants import E_D, RSC_D, calculate_P, calculate_G, int_to_arr,convert_to_six_digits


def generate_P_G_Q(sender: str, receiver: str):
    G = []
    P = []
    Q = []
    s_arr = sender.split(".")
    r_arr = receiver.split(".")
    if len(s_arr) != len(r_arr):
        return "Invalid"
    iterator = 0
    for s, r in zip(s_arr, r_arr):
        iterator += int(s) - int(r)
    sign = iterator / abs(iterator)
    iter_array = int_to_arr(iterator)
    e = int_to_arr(E_D)
    rc = int_to_arr(RSC_D)
    final_iterator = 0
    for i in iter_array:
        final_iterator = final_iterator * 10 + e[i]
    final_iterator = int(final_iterator * sign)
    G.append(calculate_G(final_iterator, 3, 4))
    P.append(calculate_P(G[0])+1)
    for i in range(1, 10):
        digits = int_to_arr(P[i - 1])
        const1 = rc[digits[len(digits) - 1]]
        const2 = rc[digits[len(digits) - 2]]
        G.append(calculate_G(G[i - 1], const1, const2))
        P.append(calculate_P(G[i]))
    for i in range(len(P)):
        if i % 2 == 0:
            Q.append(P[i])
        else:
            Q.append(P[len(P) - i])
    return G, P, Q






