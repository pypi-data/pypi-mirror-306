import re
from typing import Any, OrderedDict
from commitizen import config, defaults
from commitizen.cz.base import BaseCommitizen
from commitizen.cz.utils import multiple_line_breaker, required_validator

__all__ = ["BreveCzConventional"]


def parse_subject(text):
    if isinstance(text, str):
        text = text.strip(".").strip()

    return required_validator(text, msg="Subject is required.")


a = defaults.bump_pattern


class BreveCommitType:
    value: str
    name: str


class BreveCzConventionalConfiguration:
    # region Constants
    QUESTION_TITLES = {
        "en": {
            "change_type": "Select the type of change you are committing",
            "scope": (
                "What is the scope of this change? (file name, package name, function, setting scope, etc.) "
                "[ENTER to skip]"
            ),
            "subject": (
                "Write a short, imperative tense description of the change (lowercase, no periods)"
                "\nFor example: add feature xyz, fix bug 123, deprecate abc"
            ),
            "body": (
                "Write a longer description of the change. Feel free to use gitmoji for each sentence. "
                "[ENTER to skip]\n"
            ),
            "is_breaking_change": "Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer",
            "footer": (
                "Footer. Information about Breaking Changes and "
                "reference issues that this commit closes [ENTER to skip]\n"
            ),
        },
        "es": {
            "change_type": "Selecciona el tipo de cambio que estás realizando",
            "scope": (
                "¿Cual es el alcance de este cambio? (nombre del archivo, nombre del paquete, función, etc.) "
                "[ENTER para omitir]"
            ),
            "subject": (
                "Escribe una descripción breve del cambio, en voz pasiva (minúsculas, sin puntos)"
                "\nPor ejemplo: se agrega característica xyz, se corrige error 123, se elimina abc"
            ),
            "body": (
                "Escribe una descripción más larga del cambio. Puedes usar gitmoji para cada elemento. "
                "[ENTER para omitir]\n"
            ),
            "is_breaking_change": "¿Esto es un BREAKING CHANGE? Equivale a un cambio MAJOR en SemVer",
            "footer": (
                "Footer. Información sobre los breaking changes y "
                "referencias a los issues que cierra este commit [ENTER para omitir]\n"
            ),
        },
    }

    BASE_COMMIT_TYPES: list[str] = [
        "feat",
        "bugfix",
        "hotfix",
        "refactor",
        "perf",
        "docs",
        "test",
        "style",
        "build",
        "ci",
        "wip",
        "chore",
        "initial",
    ]

    BASE_COMMIT_DESCRIPTIONS = {
        "en": {
            "feat": "✨ A new feature was added. Correlates to MINOR in semver",
            "bugfix": "🐛 A non-critical bug was fixed. Correlates to PATCH in semver",
            "hotfix": "🚑 A critical error was fixed. Correlates to PATCH in semver",
            "refactor": "♻️ A code change that neither fixes a bug nor adds a feature.",
            "perf": "⚡ Performance improvements. Correlates to PATCH in semver",
            "docs": "📝 Add or update documentation",
            "test": "✅ Add, update or pass tests",
            "style": (
                "🎨 Changes that do not affect the meaning of the code "
                "(white-space, formatting)"
                "NOT MEANT FOR UI CHANGES"
            ),
            "build": "👷 Add or update build system, dependencies, etc.",
            "ci": "💚 Add or update continuous integration system",
            "wip": (
                "🚧 Add or update work in progress, for checkpoints only. "
                "THIS MAY NOT BE THE ONLY OR LAST COMMIT IN A PULL REQUEST"
            ),
            "chore": "🔧 Other changes that don't modify src or test files.",
            "initial": "🎉 The wonderful start of your project",
        },
        "es": {
            "feat": "✨ Se agregaron nuevas características. Equivale a MINOR en semver",
            "bugfix": "🐛 Se corrigió un error no crítico. Equivale a PATCH en semver",
            "hotfix": "🚑 Se corrigió un error crítico. Equivale a PATCH en semver",
            "refactor": (
                "♻️ Se hizo un cambio que no agrega una característica ni corrige un error." "Equivale a PATCH en semver"
            ),
            "perf": "⚡ Se hicieron mejoras en rendimiento. Equivale a PATCH en semver",
            "docs": "📝 Agrega o actualiza documentación",
            "test": "✅ Agrega, actualiza o corrige pruebas que pasan",
            "style": (
                "🎨 Cambios que no afectan al significado del código "
                "(espacios en blanco, formato). "
                "NO APLICA PARA CAMBIOS EN LA INTERFAZ DE USUARIO"
            ),
            "build": "👷 Agregar o actualizar el sistema de build, dependencias, etc.",
            "ci": "💚 Agregar o actualizar el sistema de integración continua",
            "wip": (
                "🚧 Agregar o actualizar trabajo en progreso, solo para checkpoints. "
                "ESTE NO DEBE SER EL ÚLTIMO O ÚNICO COMMIT EN UNA PULL REQUEST"
            ),
            "chore": "🔧 Otros cambios que no modifican archivos de src o test.",
            "initial": "🎉 El gran inicio de tu proyecto",
        },
    }

    COMMIT_TYPE_GITMOJI = {
        "feat": ":sparkles:",
        "bugfix": ":bug:",
        "hotfix": ":ambulance:",
        "refactor": ":recycle:",
        "perf": ":zap:",
        "docs": ":memo:",
        "test": ":white_check_mark:",
        "style": ":art:",
        "build": ":construction_worker:",
        "ci": ":green_heart:",
        "wip": ":construction:",
        "chore": ":wrench:",
        "initial": ":tada:",
    }
    # endregion

    def __init__(self, lang: str = "en", use_gitmoji: bool = False):
        self.lang = lang
        self.use_gitmoji = use_gitmoji

    def get_bump_pattern(self) -> str:
        return (
            (
                r"(?m)^BREAKING[\-\ ]CHANGE|"
                r"^(:sparkles: feat|:bug: bugfix|:ambulance: hotfix|:recycle: refactor|:zap: perf)"
            )
            if self.use_gitmoji
            else r"(?m)^BREAKING[\-\ ]CHANGE|^(feat|bugfix|hotfix|refactor|perf)"
        )

    def get_bump_map(self) -> dict[str, str]:
        return (
            OrderedDict(
                (
                    (r"^.+!$", "MAJOR"),
                    (r"(?m)^BREAKING[\-\ ]CHANGE", "MAJOR"),
                    (r"^feat", "MINOR"),
                    (r"^fix", "PATCH"),
                    (r"^refactor", "PATCH"),
                    (r"^perf", "PATCH"),
                )
            )
            if not self.use_gitmoji
            else OrderedDict(
                (
                    (r"^.+!$", "MAJOR"),
                    (r"(?m)^BREAKING[\-\ ]CHANGE", "MAJOR"),
                    (r"^:sparkles: feat", "MINOR"),
                    (r"^:bug: bugfix", "PATCH"),
                    (r"^:ambulance: hotfix", "PATCH"),
                    (r"^:recycle: refactor", "PATCH"),
                    (r"^:zap: perf", "PATCH"),
                )
            )
        )

    def get_commit_parser(self) -> str:
        return (
            r"^(?P<change_type>:[\w]+: \w+)(?:\((?P<scope>[^\)]*)\))?: (?P<message>[^\n]+)"
            r"(?:\n(?!BREAKING CHANGE:)[^\n]*)*(?:\n*BREAKING CHANGE:\s*(?P<breaking>.+))?$"
        )

    def get_changelog_pattern(self) -> str:
        return self.get_bump_pattern()

    def get_change_type_map(self) -> dict[str, str]:
        base_map = {
            "feat": "Feat",
            "bugfix": "Fix",
            "hotfix": "Hotfix",
            "refactor": "Refactor",
            "perf": "Perf",
        }

        gitmoji_prefix = {
            "feat": ":sparkles:",
            "bugfix": ":bug:",
            "hotfix": ":ambulance:",
            "refactor": ":recycle:",
            "perf": ":zap:",
        }

        translations = {
            "en": {
                "feat": "✨ New features",
                "bugfix": "🐛 Bugs Fixed",
                "hotfix": "🚑 Hot fixes",
                "refactor": "♻️ Refactors",
                "perf": "⚡ Performance improvements",
            },
            "es": {
                "feat": "✨ Nuevas características",
                "bugfix": "🐛 Correcciones",
                "hotfix": "🚑 Hot fixes",
                "refactor": "♻️ Refactorizaciones",
                "perf": "⚡ Mejoras de rendimiento",
            },
        }

        result = base_map.copy()

        if self.use_gitmoji:
            result = {f"{gitmoji_prefix[k]} {k}": v for k, v in result.items()}

        if self.lang in translations:
            result.update({k: translations[self.lang][k.split()[-1]] for k in result})

        return result

    def get_questions(self) -> list[dict[str, Any]]:
        questions = [
            {
                "type": "list",
                "name": "change_type",
                "message": self.QUESTION_TITLES[self.lang]["change_type"],
                "choices": self.__get_commit_types(),
            },
            {"type": "input", "name": "scope", "message": self.QUESTION_TITLES[self.lang]["scope"], "default": ""},
            {
                "type": "input",
                "name": "subject",
                "message": self.QUESTION_TITLES[self.lang]["subject"],
                "filter": parse_subject,
            },
            {
                "type": "input",
                "name": "body",
                "message": self.QUESTION_TITLES[self.lang]["body"],
                "default": "",
                "filter": multiple_line_breaker,
            },
            {
                "type": "confirm",
                "name": "is_breaking_change",
                "message": self.QUESTION_TITLES[self.lang]["is_breaking_change"],
                "default": False,
            },
            {"type": "input", "name": "footer", "message": self.QUESTION_TITLES[self.lang]["footer"], "default": ""},
        ]
        return questions

    def __get_commit_types(self) -> list[dict[str, Any]]:
        commit_values = {}
        for commit_type in self.BASE_COMMIT_TYPES:
            if self.use_gitmoji:
                commit_values[commit_type] = f"{self.COMMIT_TYPE_GITMOJI[commit_type]} {commit_type}"
            else:
                commit_values[commit_type] = commit_type

        return [
            {
                "value": cvv,
                "name": f"{cvv}: {self.BASE_COMMIT_DESCRIPTIONS[self.lang][cvk]}",
            }
            for (cvk, cvv) in commit_values.items()
        ]


class BreveCzConventional(BaseCommitizen):
    # configuration
    conf = config.read_cfg()
    lang = conf.settings.get("lang", "en")
    use_gitmoji = conf.settings.get("use_gitmoji", False)
    bvecz_config = BreveCzConventionalConfiguration(lang, use_gitmoji)

    # direct properties
    bump_pattern = bvecz_config.get_bump_pattern()
    bump_map = bvecz_config.get_bump_map()
    commit_parser = bvecz_config.get_commit_parser()
    changelog_pattern = bvecz_config.get_changelog_pattern()
    change_type_map = bvecz_config.get_change_type_map()

    def questions(self) -> list[dict[str, Any]]:
        questions = self.bvecz_config.get_questions()
        return questions

    def example(self) -> str:
        subject = (
            "fix: correct minor typos in code"
            if self.bvecz_config.lang == "en"
            else "fix: corregir errores ortográficos en el código"
        )
        body = (
            "see the issue for details on the typos fixed"
            if self.bvecz_config.lang == "en"
            else "revisa el issue para más detalles"
        )
        footer = "closes issue #12"
        if self.bvecz_config.use_gitmoji:
            subject = "🐛 " + subject
        return f"{subject}\n" "\n" f"{body}\n" "\n" f"{footer}"

    def schema(self) -> str:
        return "<type>(<scope>): <subject>\n" "<BLANK LINE>\n" "<body>\n" "<BLANK LINE>\n" "(BREAKING CHANGE: )<footer>"

    def message(self, answers: dict[str, Any]) -> str:
        change_type = answers["change_type"]
        scope = answers["scope"]
        subject = answers["subject"]
        body = answers["body"]
        footer = answers["footer"]
        is_breaking_change = answers["is_breaking_change"]

        if scope:
            scope = f"({scope})"
        else:
            scope = ""

        if body:
            body = f"\n\n{body}"

        if is_breaking_change:
            if not footer:
                footer = "made a breaking change"
            footer = f"BREAKING CHANGE: {footer}"

        if footer:
            footer = f"\n\n{footer}"

        return f"{change_type}{scope}: {subject}{body}{footer}"

    def info(self) -> str:
        return """
BREVETECH GITMOJI COMMITIZEN TEMPLATE FOR COMMITIZEN CLI (Python).

This is a customized version of the commitizen template, based on a extended version of conventional commits, including
additional change types, Spanish localization and gitmoji support.
"""

    def schema_pattern(self):
        SIMPLE_PATTERN = r"(feat|bugfix|hotfix|refactor|perf|docs|test|style|build|ci|wip)" r"(\(\S+\))?!?:(\s.*)"

        GITMOJI_PATTERN = (
            r"(:sparkles: feat|:bug: bugfix|:ambulance: hotfix|:recycle: refactor|:zap: perf|"
            r":memo: docs|:white_check_mark: test|:art: style|:construction_worker: build|"
            r":green_heart: ci|:construction: wip)"
            r"(\(\S+\))?!?:(\s.*)"
        )

        return SIMPLE_PATTERN if not self.bvecz_config.use_gitmoji else GITMOJI_PATTERN

    def process_commit(self, commit: str) -> str:
        pat = re.compile(self.schema_pattern())
        m = re.match(pat, commit)
        if m is None:
            return ""
        return m.group(3).strip()
