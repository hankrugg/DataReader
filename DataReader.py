import pandas as pd

class DataReader:
    def __init__(self):
        self.data = pd.read_csv("2015.csv")
        self.data.dropna(inplace=True)
        self.institutionIDs = {} # Map to link the two tables together

    def makeInstitutions(self):
        # Make a column for each thing we want to track
        institutions = pd.DataFrame(columns=["Institution ID", "Institution Name", "City", "State/Province", "Country"])
        count = 0
        for index, row in self.data.iterrows():
            # Get the institution
            institution = row["ï»¿Institution"]
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

    def makeTeams(self):
        # Make a column for each thing we want to track
        teams = pd.DataFrame(columns=["Team Number", "Advisor", "Problem", "Ranking", "Institution ID"])

        count = 0
        for index, row in self.data.iterrows():
            # Get the team number
            team_number = row["Team Number"]
            if team_number not in teams['Team Number'].values:
                teams.loc[count, "Team Number"] = team_number
                teams.loc[count, "Advisor"] = row['Advisor']
                teams.loc[count, "Problem"] = row["City"]
                teams.loc[count, "Ranking"] = row["State/Province"]
                teams.loc[count, "Institution ID"] = self.institutionIDs[row["ï»¿Institution"]]
                count += 1

        # Write as CSV
        teams.to_csv("Teams.csv", index=False)



if __name__ == "__main__":
    data = DataReader()
    data.makeInstitutions()
    data.makeTeams()