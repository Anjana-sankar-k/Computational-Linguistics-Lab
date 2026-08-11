def edit_distance(s1, s2):

    m = len(s1)
    n = len(s2)

    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # If s2 is empty, delete all characters from s1
    for i in range(m + 1):
        dp[i][0] = i

    # If s1 is empty, insert all characters of s2
    for j in range(n + 1):
        dp[0][j] = j

    # Fill the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):

            if s1[i - 1] == s2[j - 1]:
                # Characters are same
                dp[i][j] = dp[i - 1][j - 1]

            else:
                # Choose minimum of:
                # Delete, Insert, Replace
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Replace
                )

    return dp[m][n]


# Example
s1 = input("Enter first string: ")
s2 = input("Enter second string: ")

distance = edit_distance(s1, s2)

print("Minimum Edit Distance:", distance)
