import random
from typing import List, Optional

class ComplimentGenerator:

    def __init__(self):
        self.compliments = [
            "You're an exceptional problem solver, {name}!",
            "{name}, your code is so elegant and efficient!",
            "You have a remarkable ability to debug complex issues, {name}!",
            "{name}, your understanding of algorithms is impressive!",
            "Your dedication to clean code practices is inspiring, {name}!",
            "{name}, you have a knack for optimizing systems!",
            "Your contributions to open source projects are invaluable, {name}!",
            "{name}, your knowledge of data structures is top-notch!",
            "You excel at writing scalable applications, {name}!",
            "{name}, your ability to learn new technologies quickly is outstanding!",
            "Your creativity in designing software architectures is amazing, {name}!",
            "{name}, you make collaboration on projects seamless!",
            "You have an exceptional eye for detail in your coding, {name}!",
            "{name}, your passion for computer science shines through your work!",
            "You consistently write maintainable and readable code, {name}!",
            "{name}, your expertise in machine learning is impressive!",
            "You have a strong grasp of computational theory, {name}!",
            "{name}, your ability to tackle challenging projects is commendable!",
            "Your skills in database management are excellent, {name}!",
            "{name}, you have a talent for creating user-friendly interfaces!",
            "You excel at integrating different technologies, {name}!",
            "{name}, your contributions enhance the entire team!",
            "You have a profound understanding of network protocols, {name}!",
            "{name}, your persistence in solving bugs is admirable!",
            "Your innovative solutions drive our projects forward, {name}!",
            "{name}, you have a great sense of software design patterns!",
            "You effectively manage version control systems, {name}!",
            "{name}, your knowledge of cybersecurity is crucial!",
            "You have an impressive ability to document your code, {name}!",
            "{name}, your leadership in project development is outstanding!",
            "You excel at writing testable and reliable code, {name}!",
            "{name}, your enthusiasm for learning keeps the team motivated!",
            "You have a talent for simplifying complex problems, {name}!",
            "{name}, your performance in code reviews is exemplary!",
            "You consistently meet deadlines with high-quality work, {name}!",
            "{name}, your ability to mentor others is invaluable!",
            "You have a strong foundation in software engineering principles, {name}!",
            "{name}, your contributions to our codebase are significant!",
            "You excel at cross-functional collaboration, {name}!",
            "{name}, your attention to detail prevents potential issues!",
            "You have a remarkable ability to innovate, {name}!",
            "{name}, your proficiency in multiple programming languages is impressive!",
            "You effectively troubleshoot and resolve system issues, {name}!",
            "{name}, your commitment to continuous improvement is inspiring!",
            "You have a great understanding of cloud computing, {name}!",
            "{name}, your ability to handle high-pressure situations is commendable!",
            "You excel at integrating APIs seamlessly, {name}!",
            "{name}, your forward-thinking approach benefits our projects!",
            "You have an exceptional ability to analyze and optimize performance, {name}!",
            "{name}, your work ethic sets a great example for the team!",
            "You excel at designing intuitive user experiences, {name}!",
            "{name}, your proficiency in front-end development is outstanding!",
            "You have a talent for bridging the gap between technical and non-technical teams, {name}!",
            "{name}, your knowledge of DevOps practices enhances our workflow!",
            "You consistently contribute valuable insights during brainstorming sessions, {name}!",
            "{name}, your ability to adapt to new challenges is impressive!",
            "You excel at maintaining code quality standards, {name}!",
            "{name}, your strategic thinking drives our projects to success!",
            "You have a remarkable ability to foresee and mitigate risks, {name}!",
            "{name}, your dedication to optimizing resource usage is commendable!",
            "You excel at automating repetitive tasks, {name}!",
            "{name}, your expertise in artificial intelligence is invaluable!",
            "You have a strong ability to integrate user feedback into your work, {name}!",
            "{name}, your skills in parallel computing enhance our system's performance!",
            "You excel at designing robust and secure systems, {name}!",
            "{name}, your passion for teaching others enriches our team!",
            "You have an exceptional ability to stay updated with the latest technologies, {name}!",
            "{name}, your proactive approach to problem-solving is admirable!",
            "You excel at creating comprehensive technical documentation, {name}!",
            "{name}, your ability to manage and prioritize tasks is impressive!",
            "You have a remarkable talent for optimizing database queries, {name}!",
            "{name}, your insights into user behavior improve our product!",
        ]

        self.translations = {
            'en': [
                "You're amazing, {name}!",
                "{name}, you make the world a better place!",
                "Your smile brightens everyone's day, {name}!",
                "You're a true friend, {name}!",
                "Your intelligence is impressive, {name}!",
                "You have a brilliant mind, {name}!",
                "{name}, your dedication is inspiring!",
                "You're a shining star, {name}!",
                "Your passion for technology is contagious, {name}!",
                "{name}, you excel in every project you undertake!",
            ],
            'es': [
                "¡Eres increíble, {name}!",
                "{name}, haces del mundo un lugar mejor!",
                "Tu sonrisa ilumina el día de todos, {name}!",
                "¡Eres un verdadero amigo, {name}!",
                "Tu inteligencia es impresionante, {name}!",
                "Tienes una mente brillante, {name}!",
                "{name}, tu dedicación es inspiradora!",
                "¡Eres una estrella brillante, {name}!",
                "Tu pasión por la tecnología es contagiosa, {name}!",
                "{name}, destacas en cada proyecto que emprendes!",
            ],
            'fr': [
                "Tu es incroyable, {name}!",
                "{name}, tu rends le monde meilleur!",
                "Ton sourire illumine la journée de tous, {name}!",
                "Tu es un véritable ami, {name}!",
                "Ton intelligence est impressionnante, {name}!",
                "Tu as un esprit brillant, {name}!",
                "{name}, ta dévotion est inspirante!",
                "Tu es une étoile brillante, {name}!",
                "Ta passion pour la technologie est contagieuse, {name}!",
                "{name}, tu excelles dans chaque projet que tu entreprends!",
            ],
            'de': [
                "Du bist unglaublich, {name}!",
                "{name}, du machst die Welt zu einem besseren Ort!",
                "Dein Lächeln erhellt den Tag aller, {name}!",
                "Du bist ein wahrer Freund, {name}!",
                "Deine Intelligenz ist beeindruckend, {name}!",
                "Du hast einen brillanten Geist, {name}!",
                "{name}, deine Hingabe ist inspirierend!",
                "Du bist ein strahlender Stern, {name}!",
                "Deine Leidenschaft für Technologie ist ansteckend, {name}!",
                "{name}, du glänzt in jedem Projekt, das du angehst!",
            ],
            'it': [
                "Sei incredibile, {name}!",
                "{name}, rendi il mondo un posto migliore!",
                "Il tuo sorriso illumina la giornata di tutti, {name}!",
                "Sei un vero amico, {name}!",
                "La tua intelligenza è impressionante, {name}!",
                "Hai una mente brillante, {name}!",
                "{name}, la tua dedizione è ispiratrice!",
                "Sei una stella splendente, {name}!",
                "La tua passione per la tecnologia è contagiosa, {name}!",
                "{name}, eccelli in ogni progetto che intraprendi!",
            ],
        }

    def compliment(self, name: str) -> str:
        self._validate_name(name)
        return random.choice(self.compliments).format(name=name)

    def personalized_compliment(self, name: str, trait: str) -> str:
        self._validate_name(name)
        self._validate_trait(trait)
        return f"{name}, your {trait} is truly remarkable!"

    def multi_compliment(self, name: str, count: int) -> List[str]:
        self._validate_name(name)
        self._validate_count(count)
        return [self.compliment(name) for _ in range(count)]

    def compliment_in_language(self, name: str, language: str) -> str:
        self._validate_name(name)
        self._validate_language(language)
        compliments_in_lang = self.translations.get(language.lower())
        if compliments_in_lang:
            return random.choice(compliments_in_lang).format(name=name)
        else:
            return f"Language '{language}' not supported."

    def add_compliment(self, compliment: str) -> None:
        if "{name}" not in compliment:
            raise ValueError("Compliment must include '{name}' as a placeholder.")
        self.compliments.append(compliment)

    def add_translation(self, language: str, compliments: List[str]) -> None:
        for comp in compliments:
            if "{name}" not in comp:
                raise ValueError("All compliments must include '{name}' as a placeholder.")
        self.translations[language.lower()] = compliments

    def list_languages(self) -> List[str]:
        return list(self.translations.keys())

    def _validate_name(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not name.strip():
            raise ValueError("Name cannot be empty or whitespace.")

    def _validate_trait(self, trait: str) -> None:
        if not isinstance(trait, str):
            raise TypeError("Trait must be a string.")
        if not trait.strip():
            raise ValueError("Trait cannot be empty or whitespace.")

    def _validate_count(self, count: int) -> None:
        if not isinstance(count, int):
            raise TypeError("Count must be an integer.")
        if count <= 0:
            raise ValueError("Count must be a positive integer.")

    def _validate_language(self, language: str) -> None:
        if not isinstance(language, str):
            raise TypeError("Language must be a string.")
        if not language.strip():
            raise ValueError("Language cannot be empty or whitespace.")