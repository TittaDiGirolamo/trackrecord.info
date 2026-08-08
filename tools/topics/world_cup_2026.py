#!/usr/bin/env python3
"""FIFA World Cup 2026 topic module."""

from __future__ import annotations

from typing import List


class WorldCup2026:
    name = "world_cup_2026"

    def matches(self, claim: str) -> bool:
        c = (claim or "").lower()
        return any(w in c for w in (
            "world cup", "fifa", "wc2026", "worldcup",
            "semi-final", "semifinal", "quarter-final", "quarterfinal",
            "round of 16", "group stage"
        ))

    def normalize_topic(self, claim: str) -> str:
        c = (claim or "").lower()
        if any(w in c for w in (
            "win the world cup", "wins the world cup", "to win the world cup",
            "world cup winner", "will win the tournament"
        )) or ("win" in c and "world cup" in c) or ("wins" in c and "world cup" in c):
            return "FIFA World Cup 2026 - Winner"
        if "semi" in c or "semifinal" in c:
            return "FIFA World Cup 2026 - Semifinals"
        if "quarter" in c or "quarterfinal" in c or "last eight" in c:
            return "FIFA World Cup 2026 - Quarterfinals"
        if "round of 16" in c or "last 16" in c or "round-of-16" in c:
            return "FIFA World Cup 2026 - Round of 16"
        if "group" in c and ("first" in c or "win" in c or "top" in c):
            return "FIFA World Cup 2026 - Group Stage"
        if "final" in c and "semi" not in c:
            return "FIFA World Cup 2026 - Final"
        return "FIFA World Cup 2026"

    def suggest_probability(self, claim: str) -> float:
        c = (claim or "").lower()
        if "win the world cup" in c or "wins the world cup" in c or ("win" in c and "world cup" in c):
            return 0.22
        if "semi" in c:
            return 0.35
        if "quarter" in c:
            return 0.40
        if "group" in c and ("first" in c or "win" in c or "top" in c):
            return 0.45
        return 0.30

    def suggest_resolution_criteria(self, claim: str) -> str:
        c = (claim or "").lower()
        teams = [
            "france", "spain", "england", "brazil", "argentina", "germany",
            "portugal", "netherlands", "croatia", "morocco", "usa", "mexico"
        ]
        if ("win" in c and "world cup" in c) or "winner" in c:
            for team in teams:
                if team in c:
                    return (
                        f"{team.title()} is declared the official winner of the 2026 FIFA World Cup "
                        f"by FIFA (final match result)."
                    )
            return (
                "The named team is declared the official winner of the 2026 FIFA World Cup "
                "by FIFA (final match result)."
            )
        if "semi" in c:
            return (
                "The named team appears among the four teams in the official FIFA World Cup 2026 "
                "semifinal bracket."
            )
        if "quarter" in c or "last eight" in c:
            return (
                "The named team appears among the eight teams in the official FIFA World Cup 2026 "
                "quarterfinal bracket."
            )
        if "round of 16" in c or "last 16" in c:
            return (
                "The named team appears in the official FIFA World Cup 2026 round-of-16 bracket."
            )
        if "group" in c and ("first" in c or "win" in c or "top" in c):
            return (
                "The named team finishes first in its group according to the official FIFA "
                "World Cup 2026 group standings."
            )
        return (
            "The claim is verified against the official FIFA World Cup 2026 results "
            "and tournament records."
        )

    def rationale_templates(self, claim: str, probability: float) -> list[str]:
        base = (
            f"The claim is a clear directional statement. "
            f"No numerical odds were given by the forecaster. "
            f"A probability of {probability:.2f} reflects moderate confidence "
            f"consistent with similar qualitative predictions in the dataset."
        )
        winner = (
            f"This is a repeated, directional winner pick. "
            f"No explicit probability was stated. "
            f"Pre-tournament market odds for strong contenders were typically 15–25 %. "
            f"{probability:.2f} sits in that range while remaining conservative."
        )
        cautious = (
            f"Language is directional but not emphatic. "
            f"No numerical probability was provided. "
            f"{probability:.2f} is a cautious human-elicited value that avoids over-confidence."
        )
        return [base, winner, cautious]

    _PHASE_PATTERNS = [
        ("Winner", ("win the world cup", "wins the world cup", "world cup winner", "to win the", "clear favourite", "favourites", "favorites", "lifting the trophy", "second world cup triumph")),
        ("Final", (" the final", "reaches the final", "in the final", "contested by", "decided on penalties", "final is")),
        ("Semifinals", ("semi-final", "semifinal", "semi final", "semifinals", "last four")),
        ("Quarterfinals", ("quarter-final", "quarterfinal", "quarter final", "last eight", "last-eight")),
        ("Round of 16", ("round of 16", "last-16", "last 16", "round-of-16", "r16")),
        ("Group Stage", ("group stage", "in its group", "group exit", "finishes first", "finishes second", "group-stage")),
        ("Knockout Stages", ("knockout", "deep run", "strong run", "notable", "surprise package", "dark horse", "springs a surprise")),
    ]
    _ENTITIES = [
        ("United States", ("united states", "usmnt", " u.s.", "usa")),
        ("South Korea", ("south korea", "korea republic")),
        ("Bosnia and Herzegovina", ("bosnia and herzegovina", "bosnia")),
        ("Ivory Coast", ("ivory coast", "côte d'ivoire", "cote d'ivoire")),
        ("DR Congo", ("dr congo", "democratic republic of congo")),
        ("Czechia", ("czechia", "czech republic")),
        ("Netherlands", ("netherlands", "holland")),
        ("Switzerland", ("switzerland",)), ("Argentina", ("argentina",)), ("Australia", ("australia",)),
        ("Belgium", ("belgium",)), ("Brazil", ("brazil",)), ("Canada", ("canada",)),
        ("Colombia", ("colombia",)), ("Croatia", ("croatia",)), ("Ecuador", ("ecuador",)),
        ("England", ("england",)), ("France", ("france",)), ("Germany", ("germany",)),
        ("Ghana", ("ghana",)), ("Haiti", ("haiti",)), ("Japan", ("japan",)),
        ("Mexico", ("mexico",)), ("Morocco", ("morocco",)), ("Norway", ("norway",)),
        ("Panama", ("panama",)), ("Paraguay", ("paraguay",)), ("Portugal", ("portugal",)),
        ("Qatar", ("qatar",)), ("Scotland", ("scotland",)), ("Senegal", ("senegal",)),
        ("Spain", ("spain",)), ("Sweden", ("sweden",)), ("Tunisia", ("tunisia",)),
        ("Turkey", ("turkey", "türkiye", "turkiye")), ("Uruguay", ("uruguay",)),
        ("African teams", ("african teams", "two african")),
        ("European teams", ("european teams", "two european")),
    ]

    def display_tags(self, claim: str, statement_topic: str = "") -> List[str]:
        blob = f"{claim or ''} {statement_topic or ''}".lower()
        topic = statement_topic or ""
        tags: list[str] = []
        phase_from_topic = None
        for part in [p.strip() for p in topic.split(" - ")]:
            low = part.lower()
            mapping = {"winner": "Winner", "final": "Final", "semifinals": "Semifinals",
                       "quarterfinals": "Quarterfinals", "round of 16": "Round of 16",
                       "group stage": "Group Stage", "knockout stages": "Knockout Stages"}
            if low in mapping:
                phase_from_topic = mapping[low]
                break
            if low.startswith("match result"):
                phase_from_topic = "Group Stage"
                break
        if phase_from_topic:
            tags.append(phase_from_topic)
        else:
            for label, patterns in self._PHASE_PATTERNS:
                if any(p in blob for p in patterns):
                    tags.append(label)
                    break
        entities: list[str] = []
        for part in [p.strip() for p in topic.split(" - ")]:
            if part.lower().endswith(" performance"):
                entities.append(part[: -len(" Performance")])
            if "match result" in part.lower() and "[" in part and "]" in part:
                inner = part[part.find("[")+1:part.find("]")]
                for side in inner.replace(" vs ", "|").replace(" v ", "|").split("|"):
                    if side.strip():
                        entities.append(side.strip())
        for name, patterns in self._ENTITIES:
            if any(p in blob for p in patterns) and name not in entities:
                entities.append(name)
        seen = set(tags)
        for e in entities:
            if e not in seen:
                tags.append(e); seen.add(e)
        return tags
