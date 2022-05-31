
class Election:
    def __init__(self):
        self.voter_count = 0
        self.candidates = []
        self.valid_ballots = []
        self.winner_indentified = False 
        self.sample_ballot = set()
        self.sample_ballot_characteristics = ()

    def initialize_election(self):
        self.create_candidates()
        self.get_voter_count()
        self.generate_sample_ballot()
    
    def create_candidates(self):
        candidate_selection = self.get_candidate_names()
        self.create_candidate_objects(candidate_selection)
     
    def get_candidate_names(self):
        candidates_selection = input("Enter the name of each candidate separated by commas: ").lower()
        return candidates_selection

    def create_candidate_objects(self, candidates_selection):
        list = candidates_selection.split(", ")
        for candidate in list:
            self.candidates.append(Candidate(candidate))  

    def get_voter_count(self):
        self.voter_count = int(input("Enter the number of voters: "))
    
    def generate_sample_ballot(self):
        for i in range(1, len(self.candidates)+1):
            self.sample_ballot.add(i)
        self.identify_sample_ballot_characterstics()
        
    def identify_sample_ballot_characterstics(self):
        self.len_sample_ballot = len(self.sample_ballot)
        self.max_ballot_ranking = max(self.sample_ballot)
        self.min_ballot_ranking = min(self.sample_ballot)
        self.sample_ballot_characteristics = (self.len_sample_ballot, self.max_ballot_ranking, self.min_ballot_ranking)
    
    def cast_ballots(self):
        for voter in range(self.voter_count):
            ballot = Ballot(voter)
            ballot.fill_ballot(self, voter)
            ballot.check_validity(self)
            ballot.count_ballot(self)    

    def identify_winner(self):
        while self.winner_indentified == False:
            self.tabulate_votes()
            self.check_for_winner()
            self.eliminate_losers()

    def tabulate_votes(self):
        for candidate in self.candidates: 
            candidate.top_vote_count = 0
        for ballot in self.valid_ballots:
            ranking = ballot.candidate_ranking
            index = ranking.index(min(ranking))
            self.candidates[index].receive_vote()
    
    def check_for_winner(self):
        for candidate in self.candidates:
            if candidate.top_vote_count / len(self.valid_ballots) > .5:
                print(f"{candidate.name.capitalize()} wins the election!")
                quit()

    def eliminate_losers(self):
        self.mark_least_popular()
        self.check_for_tie()
        for candidate in self.candidates:
            if candidate.unpopular == True:
                self.reallocate_votes(candidate)
                self.candidates.remove(candidate)
        
    def mark_least_popular(self):
        fewest_votes = min(candidate.top_vote_count for candidate in self.candidates)
        for candidate in self.candidates:
            if candidate.top_vote_count == fewest_votes:
                candidate.unpopular = True
    
    def check_for_tie(self):
        unpopular_candidates = [candidate for candidate in self.candidates if candidate.unpopular == True]
        if len(unpopular_candidates) == len(self.candidates):
            print(f"It's a tie! The winners are: {', '.join(self.candidates)}")
            quit()

    def reallocate_votes(self, candidate):
        index = self.candidates.index(candidate)
        for ballot in self.valid_ballots:
            del ballot.candidate_ranking[index]

class Candidate:
    def __init__(self, name):
        self.name = name
        self.top_vote_count = 0
        self.unpopular = False
    
    def receive_vote(self):
        self.top_vote_count += 1

    def eliminate(self):
        self.eliminated = True

class Ballot:
    def __init__(self, voter):
        self.voter = voter
        self.candidate_ranking = []
        self.validity = True
        self.characteristics = ()
    
    def fill_ballot(self, election, voter):
        for candidate in election.candidates:
            vote_cast = int(input(f"Voter #{voter + 1}, give {candidate.name.capitalize()} a numerical rank out of {len(election.candidates)} candidates: ").lower())
            self.candidate_ranking.append(vote_cast)   
            
    def check_validity(self, election):
            self.get_ballot_characteristics(election)
            if self.characteristics == election.sample_ballot_characteristics:
                return
            else:
                self.validity = False

    def get_ballot_characteristics(self, election):
        max_vote = float('-inf')
        min_vote = float('inf')
        for i in self.candidate_ranking:
            if not i in election.sample_ballot:
                self.validity = False
                return
            if i > max_vote:
                max_vote = i
            if i < min_vote:
                min_vote = i
        self.characteristics = (len(self.candidate_ranking), max_vote, min_vote)

    def count_ballot(self, election):
        if self.validity == True:
            election.valid_ballots.append(self)

def main():
    election = Election()
    election.initialize_election()
    election.cast_ballots()
    election.identify_winner()
    

if __name__ == '__main__':
    main()