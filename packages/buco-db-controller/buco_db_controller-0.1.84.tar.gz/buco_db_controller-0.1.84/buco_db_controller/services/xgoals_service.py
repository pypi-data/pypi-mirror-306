from buco_db_controller.models.xgoals import XGoals
from buco_db_controller.repositories.xgoals_repository import XGoalsRepository
from buco_db_controller.services.fixture_service import FixtureService


class XGoalsService:
    fbref = 'fbref'
    understat = 'understat'
    flashscore = 'flashscore'

    def __init__(self):
        self.fbref_xgoals_repository = XGoalsRepository(self.fbref)
        self.understat_xgoals_repository = XGoalsRepository(self.understat)
        self.flashscore_xgoals_repository = XGoalsRepository(self.flashscore)
        self.fixture_service = FixtureService()

    def upsert_many_fixture_xg(self, xgoals, source):
        if source == self.fbref:
            self.fbref_xgoals_repository.upsert_many_fixture_xg(xgoals)
        elif source == self.understat:
            self.understat_xgoals_repository.upsert_many_fixture_xg(xgoals)
        elif source == self.flashscore:
            self.flashscore_xgoals_repository.upsert_many_fixture_xg(xgoals)

    def get_xgoals(self, fixture_id: int) -> XGoals:
        xgoals = self.get_prioritized_xgoals([fixture_id])[0]
        return xgoals

    def get_xgoals_over_season(self, team_id: int, league_id: int, season: int) -> list[XGoals]:
        fixture_ids = self.fixture_service.get_fixture_ids(team_id, league_id, season)
        return self.get_prioritized_xgoals(fixture_ids)

    def get_h2h_xgoals(self, team1_id: int, team2_id: int, league_id: int, season: int) -> list[XGoals]:
        h2h_fixture_ids = self.fixture_service.get_h2h_fixture_ids(team1_id, team2_id, league_id, season)
        return self.get_prioritized_xgoals(h2h_fixture_ids)

    def get_prioritized_xgoals(self, fixture_ids: list[int]) -> list[XGoals]:
        xgoals_data = {
            self.fbref: [XGoals.from_dict(x) for x in self.fbref_xgoals_repository.get_many_xgoals(fixture_ids)],
            self.understat: [XGoals.from_dict(x) for x in self.understat_xgoals_repository.get_many_xgoals(fixture_ids)],
            self.flashscore: [XGoals.from_dict(x) for x in self.flashscore_xgoals_repository.get_many_xgoals(fixture_ids)],
        }

        prioritized_xgoals = []
        for fixture_id in fixture_ids:
            for source in [self.fbref, self.understat, self.flashscore]:
                xgoal = next((x for x in xgoals_data[source] if x.fixture_id == fixture_id), None)
                if xgoal and xgoal.home_xg and xgoal.away_xg:
                    prioritized_xgoals.append(xgoal)
                    break

        return prioritized_xgoals
