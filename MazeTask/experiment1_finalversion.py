from psychopy import visual, core, event, gui
import pandas as pd
import random
import os
from datetime import datetime

# Load CSV files with sentences
main_df = pd.read_csv("lijst1_final_plusdistractors.csv", delimiter=";")
practice_df = pd.read_csv("oefenitems.csv", delimiter=";")
fillers_df = pd.read_csv("New_Exp_fillers.csv", delimiter=";")

# Group data by 'koppel_id' for the main experiment
units = main_df.groupby('koppel_id')
fillers = fillers_df.groupby('sentence_id')

# Display introductory screen with checkbox
consent_given = False
while not consent_given:
    intro_text = ("Welkom bij het online experiment van ons onderzoek!\n"
                  "Wij willen je vragen om anoniem deel te nemen aan ons wetenschappelijk experiment. \n" 
                  "In het experiment willen wij er graag achter komen hoe mensen bepaalde zinsstructuren verwerken.\n"
                  "Het onderzoek wordt uitgevoerd door Naomi Oppeneer (n.oppeneer@uu.nl) en Maike Sjollema (m.c.sjollema@uu.nl). \n"
                  "De eindverantwoordelijke onderzoeker is dr. Iris Mulders (i.c.m.c.mulders@uu.nl). \n\n"
                  "In dit experiment ga je zinnen lezen, één woord tegelijk. Bij elk woord krijg je twee opties te zien. \n"
                  "Kies steeds de optie die zorgt voor een grammaticaal correcte voorzetting van de zin. \n"
                  "Deelname aan het experiment duurt ongeveer 10 minuten. Er zijn geen nadelen of risico's aan verbonden. \n"
                  "Je krijgt geen vergoeding voor je deelname. \n\n"
                  "We verzamelen gegevens over de woorden die je selecteert in het experiment. Ook slaan we \n"
                  "enkele demografische gegevens op (leeftijd, geslacht, opleidingsniveau). \n"
                  "Alle gegevens worden anoniem opgeslagen en zijn alleen toegankelijk voor de uitvoerende onderzoekers en \n"
                  "de eindverantwoordelijke onderzoeker. De gegevens worden met niemand anders gedeeld. \n\n"
                  "Deelname is vrijwillig. Jouw gegevens mogen alleen voor ons onderzoek verzameld worden als je hier toestemming voor geeft. \n"
                  "Als je toch besluit niet mee te doen, hoef je verder niks te doen. Als je wel meedoet, kun je je altijd bedenken en \n"
                  "op ieder gewenst moment stoppen - ook tijdens het onderzoek. Ook na het onderzoek kun je je toestemming nog intrekken. \n\n"
                  "Als je vragen hebt over het onderzoek, kan je een e-mail sturen naar n.oppeneer@uu.nl. \n\n"
                  "Om door te gaan, vink het vakje hieronder aan en druk op OK.")

    consent_dlg = gui.Dlg(title="Informed Consent")
    consent_dlg.addText(intro_text)
    consent_dlg.addField("Ja, ik heb het bovenstaande gelezen en begrepen, en ik geef toestemming om mijn antwoorden te gebruiken voor wetenschappelijk onderzoek, zoals hierboven beschreven.", initial=False)
    user_input = consent_dlg.show()

    if not consent_dlg.OK:
        core.quit()

    consent_given = user_input[0]
    
# Collect participant information
def collect_participant_info():
    participant_info = {}
    gender_options = ["Man", "Vrouw", "Non-binair", "Wil ik niet zeggen"]
    education_options = ["Middelbare school", "MBO", "HBO", "WO Bachelor", "WO Master", "PhD"]

    dlg = gui.Dlg(title="Deelnemersinformatie")
    dlg.addField("Geboortejaar:")
    dlg.addField("Geslacht:", choices=gender_options)
    dlg.addField("Opleidingsniveau:", choices=education_options)
    user_input = dlg.show()

    if not dlg.OK:
        core.quit()

    participant_info["Geboortejaar"] = user_input[0]
    participant_info["Geslacht"] = user_input[1]
    participant_info["Opleidingsniveau"] = user_input[2]
    return participant_info

participant_info = collect_participant_info()
participant_number = random.randint(1000, 9999)

# Create a window
win = visual.Window(size=(1000, 700), color="black", fullscr=True)

# Display Instructions screen
instructions_text = ("Je gaat steeds zinnen lezen, woord voor woord. Je krijgt bij ieder woord twee opties. \n "
                     "Kies voor het woord dat zorgt voor een grammaticaal correcte voortzetting van de zin. \n "
                     "Maak hiervoor gebruik van de F en J toetsen op je computer: F voor het linkse woord"
                     "en J voor het rechtse woord.\n\n"
                     "Probeer zo snel en zo nauwkeurig mogelijk te antwoorden. \n"
                     "Gedurende het experiment is er twee keer ruimte om een paar minuten pauze te nemen. \n" 
                     "Dit wordt aangegeven op het scherm. Verder moet het experiment \n"
                     "in één keer afgemaakt worden.\n\n"
                     "Er volgen eerst drie oefenzinnen. Daarna begint het echte experiment.\n\n"
                     "Veel succes!\nKlik op de spatiebalk om door te gaan.")

instructions = visual.TextStim(win, text=instructions_text, color="white", pos=(0, 0), height=0.07)
instructions.draw()
win.flip()

# Wait for space bar press
keys = event.waitKeys(keyList=["space", "escape"])
if "escape" in keys:
    win.close()
    core.quit()

# Function to run sentences
def run_sentences(df):
    results = []
    previous_sentence_id = None
    
    for index, row in df.iterrows():
        if row["sentence_id"] != previous_sentence_id and previous_sentence_id is not None:
            next_sentence = visual.TextStim(win, text="Volgende zin", color="white", pos=(0, 0))
            next_sentence.draw()
            win.flip()
            core.wait(0.6)
        previous_sentence_id = row["sentence_id"]

        if random.random() < 0.5:
            left_word, right_word = row["correct_word"], row["incorrect_word"]
            correct_response = "f"
        else:
            left_word, right_word = row["incorrect_word"], row["correct_word"]
            correct_response = "j"

        instruction = visual.TextStim(win, text="Kies het juiste woord (F/J toetsen).", color="white", pos=(0, 0.4))
        word_left = visual.TextStim(win, text=left_word, color="white", pos=(-0.3, 0))
        word_right = visual.TextStim(win, text=right_word, color="white", pos=(0.3, 0))

        instruction.draw()
        word_left.draw()
        word_right.draw()
        win.flip()

        start_time = core.getTime()
        keys = event.waitKeys(keyList=["f", "j", "escape"])
        reaction_time = core.getTime() - start_time

        if "escape" in keys:
            win.close()
            core.quit()

        response = keys[0]
        correct = (response == correct_response)
        
        results.append([
        participant_number, participant_info["Geboortejaar"], participant_info["Geslacht"], participant_info["Opleidingsniveau"],
        row["sentence_id"], row["correct_word"], response, correct, row["condition"], row["posture_verb"], reaction_time,
        row["item_id"], row["koppel_id"], row["word_id"], row["prime_structure"], row["target_structure"], row["target_prime"],
        row["overall_id"] 
        ])

    
    next_sentence = visual.TextStim(win, text="Volgende zin", color="white", pos=(0, 0))
    next_sentence.draw()
    win.flip()
    core.wait(0.6)
    
    return results

# Run practice trials
practice_results = run_sentences(practice_df)

# Display transition screen after practice
transition_text = "Dit waren alle oefenzinnen. Nu begint het echte experiment. Druk op de spatiebalk om door te gaan."
transition_screen = visual.TextStim(win, text=transition_text, color="white", pos=(0, 0), height=0.07)
transition_screen.draw()
win.flip()
event.waitKeys(keyList=["space"])

# Shuffle main experiment units
unit_list = [(koppel_id, group) for koppel_id, group in units]
random.shuffle(unit_list)

# Select and insert fillers
all_fillers = list(fillers)
random.shuffle(all_fillers)
selected_fillers = all_fillers[:110]

experiment_results = []

# Keep track of the total sentences processed
total_sentences = 0

# Run main experiment with fillers after each unit
total_fillers_used = 0
for koppel_id, unit_df in unit_list:
    experiment_results.extend(run_sentences(unit_df.sort_values(by="sentence_id")))
    total_sentences += len(unit_df)
    
    # Check if it's time for a break (after 45th sentence, unless it's a new unit)
    if total_sentences > 85 and (total_sentences - len(unit_df)) <= 85:
        break_screen_text = "Je kunt nu een korte pauze nemen. Als je klaar bent om door te gaan, druk dan op de spatiebalk."
        break_screen = visual.TextStim(win, text=break_screen_text, color="white", pos=(0, 0), height=0.07)
        break_screen.draw()
        win.flip()
        event.waitKeys(keyList=["space"])

    # Check if it's time for a break (after 90th sentence, unless it's a new unit)
    if total_sentences > 150 and (total_sentences - len(unit_df)) <= 150:
        break_screen_text = "Je kunt nu een korte pauze nemen. Als je klaar bent om door te gaan, druk dan op de spatiebalk."
        break_screen = visual.TextStim(win, text=break_screen_text, color="white", pos=(0, 0), height=0.07)
        break_screen.draw()
        win.flip()
        event.waitKeys(keyList=["space"])

    # Insert fillers after each unit
    num_fillers = min(3, max(2, 110 - total_fillers_used))
    for _ in range(num_fillers):
        if total_fillers_used < 110 and selected_fillers:
            experiment_results.extend(run_sentences(selected_fillers.pop(0)[1]))
            total_fillers_used += 1

# Display final screen after the experiment
final_screen_text = "Je bent nu aan het einde van het experiment. Je data zijn opgeslagen. Bedankt voor je deelname!"
final_screen = visual.TextStim(win, text=final_screen_text, color="white", pos=(0, 0), height=0.07)
final_screen.draw()
win.flip()
event.waitKeys(keyList=["space"])

# Save results
participant_id = datetime.now().strftime("%Y%m%d%H%M%S")
output_folder = "experiment 1"
os.makedirs(output_folder, exist_ok=True)  # Create 'experiment 1' folder if it doesn't exist
output_file = os.path.join(output_folder, f"experiment_results_{participant_id}.csv")

# Now correctly append the results and save the dataframe to CSV
results = practice_results + experiment_results
df = pd.DataFrame(results, columns=[
    "ParticipantNumber", "Geboortejaar", "Geslacht", "Opleidingsniveau", "sentence_id", "correct_word", "response", "correct",
    "condition", "posture_verb", "reaction_time", "item_id", "koppel_id", "word_id", "prime_structure", "target_structure",
    "target_prime", "overall_id"
])

df.to_csv(output_file, index=False, sep=";")

win.close()
core.quit()