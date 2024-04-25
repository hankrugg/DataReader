import pandas as pd
import numpy as np
def average(values):
    return sum(values) / len(values)

def get_key_by_value(dictionary, target_value):
    matches = []
    for key, value in dictionary.items():
        if value == target_value:
            matches.append(key)
    return matches

def sortDict(dictionary):
    newDict = {}
    for i in range(max(dictionary.values()), 0, -1):
        if i in dictionary.values():
            matches = get_key_by_value(dictionary, i)
            for match in matches:
                newDict[match] = i
    return newDict

class DataReader:
    def __init__(self):
        self.data = pd.read_csv("2015.csv")
        self.data.dropna(inplace=True)
        # Map to link the two tables together
        self.institutionIDs = {}

    def clean_data(self):
        newData = pd.DataFrame(columns=['Institution Name', 'Team Number', 'City', 'State/Province', 'Country', 'Advisor', 'Problem', 'Ranking'])
        for index, row in self.data.iterrows():
            newData.loc[index, "Institution Name"] = self.data.loc[index]['ï»¿Institution'].lower().replace("  ", " ").strip()
            newData.loc[index, "City"] = self.data.loc[index]['City'].lower().replace("  ", " ").strip()
            newData.loc[index, "Team Number"] = self.data.loc[index]['Team Number']
            newData.loc[index, "State/Province"] = row["State/Province"] = self.data.loc[index]['State/Province'].lower().replace("  ", " ").strip()
            newData.loc[index, "Country"] = row["Country"] = self.data.loc[index]['Country'].lower().replace("  ", " ").strip()
            newData.loc[index, "Advisor"] = self.data.loc[index]['Advisor'].lower().replace("  ", " ").strip()
            newData.loc[index, "Problem"] = self.data.loc[index]['Problem'].lower().replace("  ", " ").strip()
            newData.loc[index, "Ranking"] = self.data.loc[index]['Ranking']

        return newData


    def makeInstitutions(self, data):
        # Make a column for each thing we want to track
        institutions = pd.DataFrame(columns=["Institution ID", "Institution Name", "City", "State/Province", "Country"])
        count = 0
        for index, row in data.iterrows():
            # Get the institution
            institution = row["Institution Name"]
            # If it isn't already in the institution values, add it
            if institution not in institutions['Institution Name'].values:
                institutions.loc[count, "Institution Name"] = institution
                institutions.loc[count, "Institution ID"] = count
                institutions.loc[count, "City"] = row["City"]
                institutions.loc[count, "State/Province"] = row["State/Province"]
                institutions.loc[count, "Country"] = row["Country"]
                # Add the institution and its ID to the map
                self.institutionIDs[institution] = count
                count += 1

        # Write it as a CSV
        institutions.to_csv("Institutions.csv", index=False)
        return institutions

    def makeTeams(self, data):
        # Make a column for each thing we want to track
        teams = pd.DataFrame(columns=["Team Number", "Advisor", "Problem", "Ranking", "Institution ID"])

        count = 0
        for index, row in data.iterrows():
            # Get the team number
            team_number = row["Team Number"]
            if team_number not in teams['Team Number'].values:
                teams.loc[count, "Team Number"] = team_number
                teams.loc[count, "Advisor"] = row['Advisor']
                teams.loc[count, "Problem"] = row["Problem"]
                teams.loc[count, "Ranking"] = row["Ranking"]
                teams.loc[count, "Institution ID"] = self.institutionIDs[row["Institution Name"]]
                count += 1

        # Write as CSV
        teams.to_csv("Teams.csv", index=False)
        return teams

    def getTeamStats(self, data):
        teams = data['Institution Name']
        counts = {}

        for id in teams:
            if id not in counts:
                counts[id] = 1
            else:
                counts[id] += 1
        # Average number of teams
        avgNumTeams = str(average(counts.values()))

        # List sorted by the amount of teams each institution had and the amount of teams the institution had
        numTeams = sortDict(counts)

        outstanding = str((data[data['Ranking'] == 'Outstanding Winner']['Institution Name'].sort_values()).to_numpy())

        us = (data[data['Country'] == 'usa'][['Team Number', 'Ranking']])

        usFiltered = str(us[(us['Ranking'] == 'Outstanding Winner') | (us['Ranking'] == 'Finalist') | (us['Ranking'] == 'Meritorious')].to_numpy())

        with open('Stats.txt', 'w') as file:
            file.write("Average number of teams per institution: {}\n".format(avgNumTeams))
            file.write("\nNumber of teams per institution:\n")
            for institution, count in numTeams.items():
                file.write("{}: {}\n".format(institution, count))
            file.write("\nOutstanding winners:\n")
            for winner in outstanding:
                file.write("{}".format(winner))
            file.write("\nUS teams ranking Meritorious or Better:\n")
            for team in usFiltered:
                file.write("{}".format(team))


if __name__ == "__main__":
    data = DataReader()
    cleanData = data.clean_data()
    data.makeInstitutions(cleanData)
    teams = data.makeTeams(cleanData)
    data.getTeamStats(cleanData)