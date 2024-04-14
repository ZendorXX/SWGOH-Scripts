# for unit search

with open('in-out/in.txt', 'r') as in_file:
    text = in_file.read()

data = list(text.split('\n'))

trash = [
    '--',
    'Imbued Lightsaber StrikeForce Energy', 
    'Boundless Force ThrowForce RepulseThere is Much Conflict in You', 
    'There is Much Conflict in You',
    'Family LegacyRedeemedForce Dyad',
    'ObscuredForce Dyad',
    'Fett Legacy',
    'Dangerous ReputationFett Legacy',
    'Dual Barrage',
    'Fervent RushSeething RageBound By Hatred',
    'Shaman\'s Insight',
    'RampageNightsister Swiftness',
    'Rampage',
    'Snipers ExpertiseGame Plan',
    'Game Plan',
    'Jedi Council',
    'Aggressive Tactician',
    'Dauntless',
    'ID9 Enemy Intelligence',
    'ID9 Enemy IntelligenceGuess Again',
    'Homicidal Counterpart',
    'Grizzled Veteran',
    'Return Fire',
    'Keen Eye',
    'Self-ReconstructionLoyalty to the Maker',
    'Self-Reconstruction',
    'I Don\'t Want to Kill You Per SeThat\'s Just Good Business',
    'That\'s Just Good Business',
    'Ultimate PredatorInfiltrate and Disrupt',
    'The Emperor\'s Hand',
    'Brute',
    'Everyone is Expendable',
    'They Will Never Be Victorious'
]

with open('in-out/out.txt', 'w') as out_file:
    for i in range(len(data)):
        if data[i][0].isdigit() or data[i] in trash: 
            continue

        out_file.write(f'{data[i]}\n')