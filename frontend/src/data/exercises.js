const EXERCISES = {
  id: '0',
  title: 'Welcome on board!',
  description: 'Exercise A: Time and organisation management',
  afterword: '',
  time: '5', // countdown time in minutes
  introduction:
    '# Vacuus et Athenae in fervoribus essent stamina \n## Videntur echidnae colorem sorores praestructa Liber cavus \n\nLorem markdownum animi, voce mihi aenae qui lumen hostem Hyleusque tangit. Haec\nortus conplectitur respondit nullo rapida foedere Lycisce castique, aret est\nNoctisque. **Pone suas** sic! Mihi ante vasta curvamine praesentem raptatur\nbarba sternere promissa in flexo.\n',
  profileForm: [
    {
      id: 432,
      question: 'How old are you',
      questionType: 'number',
      required: true,
    },
    {
      id: 434,
      question: 'How do you feel about privacy?',
      questionType: 'string',
      required: false,
    },
    {
      id: 435,
      question: 'Job Role',
      questionType: 'string',
      required: true,
    },
  ],
  emailRevealTimes: [
    {
      emailId: 'fa59b235-184f-40ba-aae7-daaf48689d22',
      revealTime: 5,
    },
  ],
};

export function loadExercise() {
  return EXERCISES;
}
