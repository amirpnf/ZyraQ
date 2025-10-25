export default {
  clear() {
    window.localStorage.clear();
  },
  savePlayerName(playerName) {
    window.localStorage.setItem('playerName', playerName);
  },
  getPlayerName() {
    return window.localStorage.getItem('playerName');
  },
  saveParticipationScore(participationScore) {
    window.localStorage.setItem(
      'participationScore',
      JSON.stringify(participationScore)
    );
  },
  getParticipationScore() {
    const score = window.localStorage.getItem('participationScore');
    return score ? JSON.parse(score) : null;
  },
  saveAnswers(answers) {
    window.localStorage.setItem('answers', JSON.stringify(answers));
  },
  getAnswers() {
    const answers = window.localStorage.getItem('answers');
    return answers ? JSON.parse(answers) : [];
  },
};
