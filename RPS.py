# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
import random
def player1(prev_play, opponent_history=[]):
    opponent_history.append(prev_play)
    guess = "R"
    if len(opponent_history) > 2:
        guess = opponent_history[-2]
    return guess

#Doesn't work very well doing probability based on previous
probs = {"R": 3, "P": 3, "S": 3}
def player_probs(prev_play, opponent_history=[]):
    opponent_history.append(prev_play)
    beats_it = {"R": "P", "P": "S", "S": "R"}
    if prev_play == "":
      return "P"
    probs[prev_play] += 1
    probs_swap = {v:k for k,v in probs.items()}
    #print(probs_swap[max(probs_swap.keys())])
    return beats_it[probs_swap[max(probs_swap.keys())]]


#Markov-chain
class MarkovChain():
  def __init__(self, decay):
    self.matrix = self.create_matrix()
    self.decay = decay

  def create_matrix(self):
    keys = ["PP", "PR", "PS", "RP", "RR", "RS", "SP", "SR", "SS"]
    matrix = {}
    for key in keys:
      matrix[key] = {"P": {'prob' : 1 / 3, 'n_obs' : 0},
                     "R": {'prob' : 1 / 3, 'n_obs' : 0},
                     "S": {'prob' : 1 / 3, 'n_obs' : 0}}
    return matrix

  def reset_matrix(self):
    self.matrix = self.create_matrix()

  def update_matrix(self,last_curr,prev_play):
    total = 1
    for i in self.matrix[last_curr].keys():
      self.matrix[last_curr][i]['n_obs'] *= self.decay
      total += self.matrix[last_curr][i]['n_obs']
    self.matrix[last_curr][prev_play]['n_obs'] += 1
    for i in self.matrix[last_curr].keys():
      self.matrix[last_curr][i]['prob'] = self.matrix[last_curr][i]['n_obs'] / total   

  def predict(self, last_curr):
    probs = self.matrix[last_curr]
    vals = []
    for i in probs.keys():
      vals.append(probs[i]['prob'])
    if max(vals) == min(vals):
      return random.choice(['R', 'P', 'S'])
    else:
      vals_1 = [(i[1], i[0]) for i in probs.items()]
      vals_2 = [(i['prob'],v) for i,v in vals_1]
      return max(vals_2)[1]
    
chain = MarkovChain(0.3)
beats_it = {"R": "P", "P": "S", "S": "R"}
#print(chain.matrix)
output = ""
#MARKOV CHAIN still only about 50%
#Can beat Quincey and Mugresh
#Cannot beat abbey and kris more than half the time
def player_m(prev_play, opponent_history=[]):
  if (prev_play == ""):
    opponent_history = []
    chain.reset_matrix()
    output = ""
  opponent_history.append(prev_play)
  in_out = ""
  if len(opponent_history) > 2:
    in_out = opponent_history[-2]+opponent_history[-1]
    chain.update_matrix(in_out,prev_play)
    output = beats_it[chain.predict(in_out)]
  else:
    output = beats_it[chain.predict("PP")]
  return output

#gonna play like abbey

"""abbey(prev_opponent_play,
          opponent_history=[],
          play_order=[{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }]):

    if not prev_opponent_play:
        prev_opponent_play = 'R'
    opponent_history.append(prev_opponent_play)

    last_two = "".join(opponent_history[-2:])
    if len(last_two) == 2:
        play_order[0][last_two] += 1

    potential_plays = [
        prev_opponent_play + "R",
        prev_opponent_play + "P",
        prev_opponent_play + "S",
    ]

    sub_order = {
        k: play_order[0][k]
        for k in potential_plays if k in play_order[0]
    }

    prediction = max(sub_order, key=sub_order.get)[-1:]

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prediction]
"""
"""play_order=[{
              "RRR": 0, "RRP": 0, "RRS": 0,
              "RPR": 0, "RPP": 0, "RPS": 0,
              "RSR": 0, "RSP": 0, "RSS": 0,
              "PRR": 0, "PRP": 0, "PRS": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }]"""
#three back beats everyone over 60% except abbey(55ish)
def player3(prev_play, opponent_history=[],play_order = {"RRR": 0, "RRP": 0, "RRS": 0, 
                                                        "RPR": 0, "RPP": 0, "RPS": 0, 
                                                        "RSR": 0, "RSP": 0, "RSS": 0,
                                                        "PRR": 0, "PRP": 0, "PRS": 0, 
                                                        "PPR": 0, "PPP": 0, "PPS": 0, 
                                                        "PSR": 0, "PSP": 0, "PSS": 0, 
                                                        "SRR": 0, "SRP": 0, "SRS": 0, 
                                                        "SPR": 0, "SPP": 0, "SPS": 0, 
                                                        "SSR": 0, "SSP": 0, "SSS": 0}):
  if not prev_play:
    prev_play = 'R'
    play_order = {"RRR": 0, "RRP": 0, "RRS": 0,
                  "RPR": 0, "RPP": 0, "RPS": 0,
                  "RSR": 0, "RSP": 0, "RSS": 0,
                  "PRR": 0, "PRP": 0, "PRS": 0, 
                  "PPR": 0, "PPP": 0, "PPS": 0, 
                  "PSR": 0, "PSP": 0, "PSS": 0, 
                  "SRR": 0, "SRP": 0, "SRS": 0, 
                  "SPR": 0, "SPP": 0, "SPS": 0, 
                  "SSR": 0, "SSP": 0, "SSS": 0}
  opponent_history.append(prev_play)
  last_three = "".join(opponent_history[-3:])
  if len(last_three) == 3:
        play_order[last_three] += 1
  if len(opponent_history) >= 2:
    potential_plays = ["".join(opponent_history[-2:]) + "R", "".join(opponent_history[-2:]) + "P", "".join(opponent_history[-2:]) + "S"]
    sub_plays = {k: play_order[k]
        for k in potential_plays if k in play_order}
    prediction = max(sub_plays, key=sub_plays.get)[-1:]
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prediction]
  return random.choice(["R","P","S"])
      
#last4 only beats abbey 57ish
def player4(prev_play, opponent_history=[],play_order = {"RRRR": 0, "RRRP": 0, "RRRS": 0,
                                                        "RRPR": 0, "RRPP": 0, "RRPS": 0, 
                                                        "RRSR": 0, "RRSP": 0, "RRSS": 0, 
                                                        "RPRR": 0, "RPRP": 0, "RPRS": 0, 
                                                        "RPPR": 0, "RPPP": 0, "RPPS": 0,
                                                        "RPSR": 0, "RPSP": 0, "RPSS": 0, 
                                                        "RSRR": 0, "RSRP": 0, "RSRS": 0,
                                                        "RSPR": 0, "RSPP": 0, "RSPS": 0,
                                                        "RSSR": 0, "RSSP": 0, "RSSS": 0,
                                                        "PRRR": 0, "PRRP": 0, "PRRS": 0,
                                                        "PRPR": 0, "PRPP": 0, "PRPS": 0,
                                                        "PRSR": 0, "PRSP": 0, "PRSS": 0, 
                                                        "PPRR": 0, "PPRP": 0, "PPRS": 0,
                                                        "PPPR": 0, "PPPP": 0, "PPPS": 0,
                                                        "PPSR": 0, "PPSP": 0, "PPSS": 0, 
                                                        "PSRR": 0, "PSRP": 0, "PSRS": 0, 
                                                        "PSPR": 0, "PSPP": 0, "PSPS": 0, 
                                                        "PSSR": 0, "PSSP": 0, "PSSS": 0, 
                                                        "SRRR": 0, "SRRP": 0, "SRRS": 0,
                                                        "SRPR": 0, "SRPP": 0, "SRPS": 0, 
                                                        "SRSR": 0, "SRSP": 0, "SRSS": 0,
                                                        "SPRR": 0, "SPRP": 0, "SPRS": 0, 
                                                        "SPPR": 0, "SPPP": 0, "SPPS": 0, 
                                                        "SPSR": 0, "SPSP": 0, "SPSS": 0,
                                                        "SSRR": 0, "SSRP": 0, "SSRS": 0,
                                                        "SSPR": 0, "SSPP": 0, "SSPS": 0, 
                                                        "SSSR": 0, "SSSP": 0, "SSSS": 0}):
  if not prev_play:
    prev_play = 'R'
    play_order = {"RRRR": 0, "RRRP": 0, "RRRS": 0,
                  "RRPR": 0, "RRPP": 0, "RRPS": 0, 
                  "RRSR": 0, "RRSP": 0, "RRSS": 0, 
                  "RPRR": 0, "RPRP": 0, "RPRS": 0, 
                  "RPPR": 0, "RPPP": 0, "RPPS": 0,
                  "RPSR": 0, "RPSP": 0, "RPSS": 0, 
                  "RSRR": 0, "RSRP": 0, "RSRS": 0,
                  "RSPR": 0, "RSPP": 0, "RSPS": 0,
                  "RSSR": 0, "RSSP": 0, "RSSS": 0,
                  "PRRR": 0, "PRRP": 0, "PRRS": 0,
                  "PRPR": 0, "PRPP": 0, "PRPS": 0,
                  "PRSR": 0, "PRSP": 0, "PRSS": 0, 
                  "PPRR": 0, "PPRP": 0, "PPRS": 0,
                  "PPPR": 0, "PPPP": 0, "PPPS": 0,
                  "PPSR": 0, "PPSP": 0, "PPSS": 0,
                  "PSRR": 0, "PSRP": 0, "PSRS": 0,
                  "PSPR": 0, "PSPP": 0, "PSPS": 0, 
                  "PSSR": 0, "PSSP": 0, "PSSS": 0, 
                  "SRRR": 0, "SRRP": 0, "SRRS": 0,
                  "SRPR": 0, "SRPP": 0, "SRPS": 0,
                  "SRSR": 0, "SRSP": 0, "SRSS": 0,
                  "SPRR": 0, "SPRP": 0, "SPRS": 0,
                  "SPPR": 0, "SPPP": 0, "SPPS": 0,
                  "SPSR": 0, "SPSP": 0, "SPSS": 0,
                  "SSRR": 0, "SSRP": 0, "SSRS": 0,
                  "SSPR": 0, "SSPP": 0, "SSPS": 0,
                  "SSSR": 0, "SSSP": 0, "SSSS": 0}
  opponent_history.append(prev_play)
  last_four = "".join(opponent_history[-4:])
  if len(last_four) == 4:
        play_order[last_four] += 1
  if len(opponent_history) >= 3:
    potential_plays = ["".join(opponent_history[-3:]) + "R", "".join(opponent_history[-3:]) + "P", "".join(opponent_history[-3:]) + "S"]
    sub_plays = {k: play_order[k]
        for k in potential_plays if k in play_order}
    prediction = max(sub_plays, key=sub_plays.get)[-1:]
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prediction]
  return random.choice(["R","P","S"])
#last 5 gives over 60 for abbey
def player(prev_play, opponent_history=[],play_order = {"RRRRR": 0, "RRRRP": 0, "RRRRS": 0,
                                                        "RRRPR": 0, "RRRPP": 0, "RRRPS": 0,
                                                        "RRRSR": 0, "RRRSP": 0, "RRRSS": 0,
                                                        "RRPRR": 0, "RRPRP": 0, "RRPRS": 0,
                                                        "RRPPR": 0, "RRPPP": 0, "RRPPS": 0,
                                                        "RRPSR": 0, "RRPSP": 0, "RRPSS": 0, 
                                                        "RRSRR": 0, "RRSRP": 0, "RRSRS": 0, 
                                                        "RRSPR": 0, "RRSPP": 0, "RRSPS": 0,
                                                        "RRSSR": 0, "RRSSP": 0, "RRSSS": 0,
                                                        "RPRRR": 0, "RPRRP": 0, "RPRRS": 0,
                                                        "RPRPR": 0, "RPRPP": 0, "RPRPS": 0,
                                                        "RPRSR": 0, "RPRSP": 0, "RPRSS": 0,
                                                        "RPPRR": 0, "RPPRP": 0, "RPPRS": 0,
                                                        "RPPPR": 0, "RPPPP": 0, "RPPPS": 0,
                                                        "RPPSR": 0, "RPPSP": 0, "RPPSS": 0,
                                                        "RPSRR": 0, "RPSRP": 0, "RPSRS": 0,
                                                        "RPSPR": 0, "RPSPP": 0, "RPSPS": 0,
                                                        "RPSSR": 0, "RPSSP": 0, "RPSSS": 0,
                                                        "RSRRR": 0, "RSRRP": 0, "RSRRS": 0,
                                                        "RSRPR": 0, "RSRPP": 0, "RSRPS": 0,
                                                        "RSRSR": 0, "RSRSP": 0, "RSRSS": 0,
                                                        "RSPRR": 0, "RSPRP": 0, "RSPRS": 0,
                                                        "RSPPR": 0, "RSPPP": 0, "RSPPS": 0,
                                                        "RSPSR": 0, "RSPSP": 0, "RSPSS": 0,
                                                        "RSSRR": 0, "RSSRP": 0, "RSSRS": 0,
                                                        "RSSPR": 0, "RSSPP": 0, "RSSPS": 0,
                                                        "RSSSR": 0, "RSSSP": 0, "RSSSS": 0,
                                                        "PRRRR": 0, "PRRRP": 0, "PRRRS": 0,
                                                        "PRRPR": 0, "PRRPP": 0, "PRRPS": 0,
                                                        "PRRSR": 0, "PRRSP": 0, "PRRSS": 0,
                                                        "PRPRR": 0, "PRPRP": 0, "PRPRS": 0,
                                                        "PRPPR": 0, "PRPPP": 0, "PRPPS": 0,
                                                        "PRPSR": 0, "PRPSP": 0, "PRPSS": 0,
                                                        "PRSRR": 0, "PRSRP": 0, "PRSRS": 0,
                                                        "PRSPR": 0, "PRSPP": 0, "PRSPS": 0,
                                                        "PRSSR": 0, "PRSSP": 0, "PRSSS": 0,
                                                        "PPRRR": 0, "PPRRP": 0, "PPRRS": 0,
                                                        "PPRPR": 0, "PPRPP": 0, "PPRPS": 0,
                                                        "PPRSR": 0, "PPRSP": 0, "PPRSS": 0,
                                                        "PPPRR": 0, "PPPRP": 0, "PPPRS": 0,
                                                        "PPPPR": 0, "PPPPP": 0, "PPPPS": 0,
                                                        "PPPSR": 0, "PPPSP": 0, "PPPSS": 0,
                                                        "PPSRR": 0, "PPSRP": 0, "PPSRS": 0,
                                                        "PPSPR": 0, "PPSPP": 0, "PPSPS": 0,
                                                        "PPSSR": 0, "PPSSP": 0, "PPSSS": 0,
                                                        "PSRRR": 0, "PSRRP": 0, "PSRRS": 0,
                                                        "PSRPR": 0, "PSRPP": 0, "PSRPS": 0,
                                                        "PSRSR": 0, "PSRSP": 0, "PSRSS": 0,
                                                        "PSPRR": 0, "PSPRP": 0, "PSPRS": 0,
                                                        "PSPPR": 0, "PSPPP": 0, "PSPPS": 0,
                                                        "PSPSR": 0, "PSPSP": 0, "PSPSS": 0,
                                                        "PSSRR": 0, "PSSRP": 0, "PSSRS": 0,
                                                        "PSSPR": 0, "PSSPP": 0, "PSSPS": 0,
                                                        "PSSSR": 0, "PSSSP": 0, "PSSSS": 0,
                                                        "SRRRR": 0, "SRRRP": 0, "SRRRS": 0,
                                                        "SRRPR": 0, "SRRPP": 0, "SRRPS": 0,
                                                        "SRRSR": 0, "SRRSP": 0, "SRRSS": 0,
                                                        "SRPRR": 0, "SRPRP": 0, "SRPRS": 0,
                                                        "SRPPR": 0, "SRPPP": 0, "SRPPS": 0,
                                                        "SRPSR": 0, "SRPSP": 0, "SRPSS": 0,
                                                        "SRSRR": 0, "SRSRP": 0, "SRSRS": 0,
                                                        "SRSPR": 0, "SRSPP": 0, "SRSPS": 0,
                                                        "SRSSR": 0, "SRSSP": 0, "SRSSS": 0,
                                                        "SPRRR": 0, "SPRRP": 0, "SPRRS": 0,
                                                        "SPRPR": 0, "SPRPP": 0, "SPRPS": 0,
                                                        "SPRSR": 0, "SPRSP": 0, "SPRSS": 0,
                                                        "SPPRR": 0, "SPPRP": 0, "SPPRS": 0,
                                                        "SPPPR": 0, "SPPPP": 0, "SPPPS": 0,
                                                        "SPPSR": 0, "SPPSP": 0, "SPPSS": 0,
                                                        "SPSRR": 0, "SPSRP": 0, "SPSRS": 0,
                                                        "SPSPR": 0, "SPSPP": 0, "SPSPS": 0,
                                                        "SPSSR": 0, "SPSSP": 0, "SPSSS": 0,
                                                        "SSRRR": 0, "SSRRP": 0, "SSRRS": 0,
                                                        "SSRPR": 0, "SSRPP": 0, "SSRPS": 0,
                                                        "SSRSR": 0, "SSRSP": 0, "SSRSS": 0,
                                                        "SSPRR": 0, "SSPRP": 0, "SSPRS": 0,
                                                        "SSPPR": 0, "SSPPP": 0, "SSPPS": 0,
                                                        "SSPSR": 0, "SSPSP": 0, "SSPSS": 0,
                                                        "SSSRR": 0, "SSSRP": 0, "SSSRS": 0,
                                                        "SSSPR": 0, "SSSPP": 0, "SSSPS": 0,
                                                        "SSSSR": 0, "SSSSP": 0, "SSSSS": 0}):
  if not prev_play:
    prev_play = 'R'
    play_order = {"RRRRR": 0, "RRRRP": 0, "RRRRS": 0,
                  "RRRPR": 0, "RRRPP": 0, "RRRPS": 0,
                  "RRRSR": 0, "RRRSP": 0, "RRRSS": 0,
                  "RRPRR": 0, "RRPRP": 0, "RRPRS": 0,
                  "RRPPR": 0, "RRPPP": 0, "RRPPS": 0,
                  "RRPSR": 0, "RRPSP": 0, "RRPSS": 0, 
                  "RRSRR": 0, "RRSRP": 0, "RRSRS": 0, 
                  "RRSPR": 0, "RRSPP": 0, "RRSPS": 0,
                  "RRSSR": 0, "RRSSP": 0, "RRSSS": 0,
                  "RPRRR": 0, "RPRRP": 0, "RPRRS": 0,
                  "RPRPR": 0, "RPRPP": 0, "RPRPS": 0,
                  "RPRSR": 0, "RPRSP": 0, "RPRSS": 0,
                  "RPPRR": 0, "RPPRP": 0, "RPPRS": 0,
                  "RPPPR": 0, "RPPPP": 0, "RPPPS": 0,
                  "RPPSR": 0, "RPPSP": 0, "RPPSS": 0,
                  "RPSRR": 0, "RPSRP": 0, "RPSRS": 0,
                  "RPSPR": 0, "RPSPP": 0, "RPSPS": 0,
                  "RPSSR": 0, "RPSSP": 0, "RPSSS": 0,
                  "RSRRR": 0, "RSRRP": 0, "RSRRS": 0,
                  "RSRPR": 0, "RSRPP": 0, "RSRPS": 0,
                  "RSRSR": 0, "RSRSP": 0, "RSRSS": 0,
                  "RSPRR": 0, "RSPRP": 0, "RSPRS": 0,
                  "RSPPR": 0, "RSPPP": 0, "RSPPS": 0,
                  "RSPSR": 0, "RSPSP": 0, "RSPSS": 0,
                  "RSSRR": 0, "RSSRP": 0, "RSSRS": 0,
                  "RSSPR": 0, "RSSPP": 0, "RSSPS": 0,
                  "RSSSR": 0, "RSSSP": 0, "RSSSS": 0,
                  "PRRRR": 0, "PRRRP": 0, "PRRRS": 0,
                  "PRRPR": 0, "PRRPP": 0, "PRRPS": 0,
                  "PRRSR": 0, "PRRSP": 0, "PRRSS": 0,
                  "PRPRR": 0, "PRPRP": 0, "PRPRS": 0,
                  "PRPPR": 0, "PRPPP": 0, "PRPPS": 0,
                  "PRPSR": 0, "PRPSP": 0, "PRPSS": 0,
                  "PRSRR": 0, "PRSRP": 0, "PRSRS": 0,
                  "PRSPR": 0, "PRSPP": 0, "PRSPS": 0,
                  "PRSSR": 0, "PRSSP": 0, "PRSSS": 0,
                  "PPRRR": 0, "PPRRP": 0, "PPRRS": 0,
                  "PPRPR": 0, "PPRPP": 0, "PPRPS": 0,
                  "PPRSR": 0, "PPRSP": 0, "PPRSS": 0,
                  "PPPRR": 0, "PPPRP": 0, "PPPRS": 0,
                  "PPPPR": 0, "PPPPP": 0, "PPPPS": 0,
                  "PPPSR": 0, "PPPSP": 0, "PPPSS": 0,
                  "PPSRR": 0, "PPSRP": 0, "PPSRS": 0,
                  "PPSPR": 0, "PPSPP": 0, "PPSPS": 0,
                  "PPSSR": 0, "PPSSP": 0, "PPSSS": 0,
                  "PSRRR": 0, "PSRRP": 0, "PSRRS": 0,
                  "PSRPR": 0, "PSRPP": 0, "PSRPS": 0,
                  "PSRSR": 0, "PSRSP": 0, "PSRSS": 0,
                  "PSPRR": 0, "PSPRP": 0, "PSPRS": 0,
                  "PSPPR": 0, "PSPPP": 0, "PSPPS": 0,
                  "PSPSR": 0, "PSPSP": 0, "PSPSS": 0,
                  "PSSRR": 0, "PSSRP": 0, "PSSRS": 0,
                  "PSSPR": 0, "PSSPP": 0, "PSSPS": 0,
                  "PSSSR": 0, "PSSSP": 0, "PSSSS": 0,
                  "SRRRR": 0, "SRRRP": 0, "SRRRS": 0,
                  "SRRPR": 0, "SRRPP": 0, "SRRPS": 0,
                  "SRRSR": 0, "SRRSP": 0, "SRRSS": 0,
                  "SRPRR": 0, "SRPRP": 0, "SRPRS": 0,
                  "SRPPR": 0, "SRPPP": 0, "SRPPS": 0,
                  "SRPSR": 0, "SRPSP": 0, "SRPSS": 0,
                  "SRSRR": 0, "SRSRP": 0, "SRSRS": 0,
                  "SRSPR": 0, "SRSPP": 0, "SRSPS": 0,
                  "SRSSR": 0, "SRSSP": 0, "SRSSS": 0,
                  "SPRRR": 0, "SPRRP": 0, "SPRRS": 0,
                  "SPRPR": 0, "SPRPP": 0, "SPRPS": 0,
                  "SPRSR": 0, "SPRSP": 0, "SPRSS": 0,
                  "SPPRR": 0, "SPPRP": 0, "SPPRS": 0,
                  "SPPPR": 0, "SPPPP": 0, "SPPPS": 0,
                  "SPPSR": 0, "SPPSP": 0, "SPPSS": 0,
                  "SPSRR": 0, "SPSRP": 0, "SPSRS": 0,
                  "SPSPR": 0, "SPSPP": 0, "SPSPS": 0,
                  "SPSSR": 0, "SPSSP": 0, "SPSSS": 0,
                  "SSRRR": 0, "SSRRP": 0, "SSRRS": 0,
                  "SSRPR": 0, "SSRPP": 0, "SSRPS": 0,
                  "SSRSR": 0, "SSRSP": 0, "SSRSS": 0,
                  "SSPRR": 0, "SSPRP": 0, "SSPRS": 0,
                  "SSPPR": 0, "SSPPP": 0, "SSPPS": 0,
                  "SSPSR": 0, "SSPSP": 0, "SSPSS": 0,
                  "SSSRR": 0, "SSSRP": 0, "SSSRS": 0,
                  "SSSPR": 0, "SSSPP": 0, "SSSPS": 0,
                  "SSSSR": 0, "SSSSP": 0, "SSSSS": 0}
  opponent_history.append(prev_play)
  last_five = "".join(opponent_history[-5:])
  if len(last_five) == 5:
        play_order[last_five] += 1
  if len(opponent_history) >= 4:
    potential_plays = ["".join(opponent_history[-4:]) + "R", "".join(opponent_history[-4:]) + "P", "".join(opponent_history[-4:]) + "S"]
    sub_plays = {k: play_order[k]
        for k in potential_plays if k in play_order}
    prediction = max(sub_plays, key=sub_plays.get)[-1:]
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prediction]
  return random.choice(["R","P","S"])
    