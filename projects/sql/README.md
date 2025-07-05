from game_mechanics import Player, GameMechanics, LEVELS, FeedbackType, RewardType

player = Player("usuario1")
game = GameMechanics(LEVELS)

print(game.give_feedback(FeedbackType.CORRECT))
player.add_points(10)

if game.check_level_up(player):
    print(game.give_feedback(FeedbackType.LEVEL_UP))
    game.assign_reward(player, RewardType.BADGE)