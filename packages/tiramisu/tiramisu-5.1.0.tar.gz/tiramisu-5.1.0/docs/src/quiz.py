from sys import exit
from tiramisu import (MetaConfig, Config, OptionDescription,
                      BoolOption, ChoiceOption, StrOption, IntOption,
                      Calculation, Params, ParamOption,
                      default_storage, list_sessions)
from tiramisu.error import ConflictError


default_storage.setting(engine="sqlite3")


def verif(q: str, a: str):
    return q == a


def results(*verif):
    return sum(verif)


questions = [{'description': 'what does the cat say?',
              'proposal': ('woof', 'meow'),
              'answer': 'meow'},
             {'description': 'what do you get by mixing blue and yellow?',
              'proposal': ('green', 'red', 'purple'),
              'answer': 'green'},
             {'description': 'where is Bryan?',
              'proposal': ('at school', 'in his bedroom', 'in the kitchen'),
              'answer': 'in the kitchen'},
             {'description': 'which one has 4 legs and 2 wings?',
              'proposal': ('a wyvern', 'a dragon', 'a wyrm', 'a drake'),
              'answer': 'a dragon'},
             {'description': 'why life?',
              'proposal': ('because', 'I don\'t know', 'good question'),
              'answer': 'good question'},
            ]


options_obj = []
results_obj = []
for idx, question in enumerate(questions):
    idx += 1
    choice = ChoiceOption('question',
                          question['description'],
                          question['proposal'])
    answer = StrOption('answer',
                       f'Answer {idx}',
                       default=question['answer'],
                       properties=('frozen',))
    boolean = BoolOption('verif',
                         f'Verif of question {idx}',
                         Calculation(verif,
                                     Params((ParamOption(choice),
                                             ParamOption(answer)))),
                         properties=('frozen',))
    optiondescription = OptionDescription(f'question_{idx}',
                                          f'Question {idx}',
                                          [choice, answer, boolean])
    options_obj.append(optiondescription)
    results_obj.append(ParamOption(boolean))


options_obj.append(IntOption('res',
                             'Quiz results',
                             Calculation(results,
                                         Params(tuple(results_obj)))))
rootod = OptionDescription('root', '', options_obj)
meta_cfg = MetaConfig([], optiondescription=rootod, persistent=True, session_id="quiz")


def run_quiz(meta_cfg: MetaConfig):
    pseudo = input("Enter a name: ")
    try:
        cfg = meta_cfg.config.new(pseudo, persistent=True)
    except ConflictError:
        print(f'Hey {pseudo} you already answered the questionnaire')
        exit()
    cfg.property.read_write()

    for idx, question in enumerate(cfg.option.list(type='optiondescription')):
        question_id = question.option.doc()
        question_obj = question.option('question')
        question_doc = question_obj.option.doc()
        print(f'{question_id}: {question_doc}')
        print(*question_obj.value.list(), sep=" | ")
        while True:
            input_ans = input('Your answer: ')
            try:
                question_obj.value.set(input_ans)
            except ValueError as err:
                err.prefix = ''
                print(err)
            else:
                break
        if question.option('verif').value.get() is True:
            print('Correct answer!')
        else:
            print("Wrong answer... the correct answer was:", question.option('answer').value.get())
        print('')
    qno = idx + 1
    print("Correct answers:", cfg.option('res').value.get(), "out of", qno)
    if cfg.option('res').value.get() == 0 :
        print("Ouch... Maybe next time?")
    elif cfg.option('res').value.get() == qno :
        print("Wow, great job!")


def quiz_results(meta_cfg: MetaConfig):
    for cfg in meta_cfg.config.list():
        print(f"==================== {cfg.config.name()} ==========================")
        for idx, question in enumerate(cfg.option.list(type='optiondescription')):
            if question.option('verif').value.get() is True:
                answer = "correct answer"
            else:
                answer = "wrong answer: " + str(question.option('question').value.get())
            print(question.option.doc() + ': ' + answer)
        qno = idx + 1
        print(f'{cfg.config.name()}\'s score: {cfg.option("res").value.get()} out of {qno}')
    

# reload old sessions
for session_id in list_sessions():
    # our meta config is just here to be a base, so we don't want its session id to be used
    if session_id != "quiz":
        meta_cfg.config.new(session_id, persistent=True)
while True:
    who = input("Who are you? (a student | a teacher): ")
    if who in ['a student', 'a teacher']:
        break
if who == 'a student':
    run_quiz(meta_cfg)
else:
    quiz_results(meta_cfg)
