def __longest_common_subsequence(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]

def find_similar_words(target_word, word_list, threshold):
    similar_words = []
    for word in word_list:
        similarity = __longest_common_subsequence(target_word.lower(), word.lower())
        if similarity >= threshold:
            similar_words.append(word)
    return similar_words
