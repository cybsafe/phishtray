const EXERCISES = {
  id: '0',
  exercise: 'Welcome on board!',
  time: '5 minutes',
  content:
    '# Vacuus et Athenae in fervoribus essent stamina \n## Videntur echidnae colorem sorores praestructa Liber cavus \n\nLorem markdownum animi, voce mihi aenae qui lumen hostem Hyleusque tangit. Haec\nortus conplectitur respondit nullo rapida foedere Lycisce castique, aret est\nNoctisque. **Pone suas** sic! Mihi ante vasta curvamine praesentem raptatur\nbarba sternere promissa in flexo.\n',
  form: [
    {
      key: 432,
      label: 'How old are you',
      type: 'number',
    },
    {
      key: 434,
      label: 'How do you feel about privacy?',
      type: 'string',
    },
    {
      key: 435,
      label: 'Job Role',
      type: 'string',
    },
  ],
};

export function loadExercise() {
  return EXERCISES;
}
