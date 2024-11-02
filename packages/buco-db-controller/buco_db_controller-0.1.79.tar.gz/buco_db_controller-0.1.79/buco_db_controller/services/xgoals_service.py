from buco_db_controller.models.xgoals import XGoals
from buco_db_controller.repositories.xgoals_repository import XGoalsRepository
from buco_db_controller.services.fixture_service import FixtureService


class XGoalsService:
    fbref = 'fbref'
    understat = 'understat'
    flashscore = 'flashscore'

    def __init__(self, db_name):
        self.fbref_xgoals_repository = XGoalsRepository(self.fbref)
        self.understat_xgoals_repository = XGoalsRepository(self.understat)
        self.flashscore_xgoals_repository = XGoalsRepository(self.flashscore)
        self.fixture_service = FixtureService()

    def upsert_many_fixture_xg(self, xgoals):
        self.xgoals_repository.upsert_many_fixture_xg(xgoals)

    def get_xgoals(self, fixture_id: int) -> XGoals:
        xgoals = self.xgoals_repository.get_xgoals(fixture_id)
        return xgoals

    def get_xgoals_over_season(self, team_id: int, league_id: int, season: int) -> list[XGoals]:
        fixture_ids = self.fixture_service.get_fixture_ids(team_id, league_id, season)
        xgoals_over_season = self.xgoals_repository.get_many_xgoals(fixture_ids)
        xgoals_over_season = [XGoals.from_dict(response) for response in xgoals_over_season]

        return xgoals_over_season

    def get_h2h_xgoals(self, team1_id, team2_id, league_id, season) -> list[XGoals]:
        h2h_fixture_ids = self.fixture_service.get_h2h_fixture_ids(team1_id, team2_id, league_id, season)
        fbref_h2h_xgoals = self.fbref_xgoals_repository.get_many_xgoals(h2h_fixture_ids)
        understat_h2h_xgoals = self.understat_xgoals_repository.get_many_xgoals(h2h_fixture_ids)
        flashscore_h2h_xgoals = self.flashscore_xgoals_repository.get_many_xgoals(h2h_fixture_ids)

        fbref_h2h_xgoals = [XGoals.from_dict(xgoal) for xgoal in fbref_h2h_xgoals]
        understat_h2h_xgoals = [XGoals.from_dict(xgoal) for xgoal in understat_h2h_xgoals]
        flashscore_h2h_xgoals = [XGoals.from_dict(xgoal) for xgoal in flashscore_h2h_xgoals]

        priority_sources = [self.fbref, self.understat, self.flashscore]

        prior_h2h_xgoals = []
        for fixture_id in h2h_fixture_ids:
            for source in priority_sources:
                if source == self.fbref:
                    xgoal = next((xgoal for xgoal in fbref_h2h_xgoals if xgoal.fixture_id == fixture_id), None)
                elif source == self.understat:
                    xgoal = next((xgoal for xgoal in understat_h2h_xgoals if xgoal.fixture_id == fixture_id), None)
                elif source == self.flashscore:
                    xgoal = next((xgoal for xgoal in flashscore_h2h_xgoals if xgoal.fixture_id == fixture_id), None)

                if xgoal.home_xg and xgoal.away_xg:
                    prior_h2h_xgoals.append(xgoal)

        return prior_h2h_xgoals
