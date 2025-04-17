from collections import Counter

# Read all the votes from the file
with open("votes.txt", "r") as f:
    votes = [line.strip().split(": ")[1] for line in f]

# Count the votes
results = Counter(votes)

# Display the results
print("🗳 Voting Results:")
for candidate, count in results.items():
    print(f"{candidate}: {count} vote(s)")