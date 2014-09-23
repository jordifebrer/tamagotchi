from random import random, randint, shuffle


class Tamagotchi(object):
    def __init__(self):
        self.age = 0
        self.health = 20
        self.food = 20
        self.illness = 0
        self.poo = 0
        self.hangover = 0
        self.drunk = False
        self.holiday = 0

    def user_action(self, action_string):
        words = action_string.split()
        # possible actions:
        # feed, put to bed
        try:
            action = words[0]
        except IndexError:
            return

        if action.startswith("f"):
            self.food += 2
            self.poo += 1
        elif action.startswith("b"):
            self.health += 2
        elif action.startswith("c"):
            self.poo = 0

    def do_illness(self):
        # effect of illness
        if self.illness > 0:
            self.illness -= 1
            self.poo += 1
            if self.illness == 0:
                return "\nYour Tamagotchi is well again"
            else:
                return "\nYour Tamagotchi is still ill"
        return ""

    def do_hunger(self):
        # effect of hunger
        if self.food < 2:
            self.health -= 2
            return "\nYour Tamagotchi is starving"
        elif self.food < 10:
            self.health -= 1
            return "\nYour Tamagotchi is hungry"
        return ""

    def do_filth(self):
        # effect of poo
        if self.poo > 10:
            self.health -= 1
            return "\nYour Tamagotchi needs a wash"
        elif self.poo > 15:
            self.health -= 2
            return "\nYour Tamagotchi is filthy"
        return ""

    def do_hangover(self):
        if self.hangover > 0:
            self.health -= 1
            self.hangover -= 1
            return "\nYour Tamagotchi is hung over"
        return ""

    def advance(self):
        report = "Time passes"
        if self.holiday > 0:
            self.holiday -= 1
            if self.holiday == 0:
                report += "\nYour Tamagotchi came back from holiday"
            else:
                report += "\nYour Tamagotchi is still on holiday"
                return report

        self.drunk = False

        self.age += 1
        if self.illness > 0:
            self.health -= 2
        else:
            self.health -= 1
        self.food -= 1

        report += self.do_illness()
        report += self.do_hunger()
        report += self.do_filth()
        report += self.do_hangover()

        return report

    def chech_for_death(self):
        if self.health <= 0:
            return "\nYour Tamagotchi has left you for somebody that cares, at the age of {}".format(self.age)
        else:
            return ""

    event_probs = [
        (0.07, "illness"),
        (0.15, "sunny"),
        (0.1, "drunk"),
        (0.05, "holiday")
    ]

    def random_events(self):
        shuffle(self.event_probs)
        report = "Nothing happened"
        if self.holiday > 0:
            return report
        new_event = ""
        for prob, event in self.event_probs:
            if random() < prob:
                new_event = event
                break
        if new_event == "illness" and self.illness == 0:
            report = "Your Tamagotchi got ill!"
            self.illness = 5
        if new_event == "sunny":
            report = "It's a sunny day!"
            self.health += 3
        if new_event == "drunk":
            report = "Your Tamagotchi got drunk!"
            self.drunk = True
            self.hangover += 2
            self.health += 1
        if new_event == "holiday":
            self.holiday = randint(3,6)
            report = "Your Tamagotchi went on holiday"
        return report

    def state_report(self):
        report = self.bar_report("age", ">", self.age // 2)
        report += self.bar_report("health", "+", self.health)
        report += self.bar_report("food", "#", self.food)
        report += self.bar_report("poo", "$", self.poo)
        return report

    def mood_report(self):
        mood_level = self.health + self.food - 2*self.illness - self.poo
        if self.health <= 0:
            mood = "X("
        elif self.drunk:
            mood = "X)"
        elif mood_level > 35:
            mood = ":D"
        elif mood_level > 20:
            mood = ":)"
        elif mood_level > 10:
            mood = ":|"
        elif mood_level > 0:
            mood = ":("
        else:
            mood = ";["
        return "Mood: "+mood

    def bar_report(self, heading, c, level):
        if self.holiday > 0:
            return "{:10} T A M A G O T C H I - H O L I D A Y\n".format(heading)
        else:
            return "{:10} {}\n".format(heading, c*level)


divider = "\n"+"-"*20

def main():
    t = Tamagotchi()
    print("""
Welcome to the Tamagotchi simulator.
This is designed to accurately reflect the futility of existence.
Have a nice day.
""")
    print('\n'.join([divider, t.state_report(), t.mood_report()]))
    while t.health > 0:
        user_input = raw_input("bed(b), feed(f) or clean(c) --> ")
        t.user_action(user_input)
        time_report = t.advance()
        event_report = t.random_events()
        death_report = t.chech_for_death()
        print('\n'.join([divider, time_report, event_report, death_report, t.state_report(), t.mood_report()]))


if __name__ == "__main__":
    main()
