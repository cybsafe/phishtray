const EXERCISES = {
  id: '0',
  title: 'Welcome on board!',
  description: '',
  afterword: '',
  time: '5 minutes',
  introduction:
    '# Vacuus et Athenae in fervoribus essent stamina \n## Videntur echidnae colorem sorores praestructa Liber cavus \n\nLorem markdownum animi, voce mihi aenae qui lumen hostem Hyleusque tangit. Haec\nortus conplectitur respondit nullo rapida foedere Lycisce castique, aret est\nNoctisque. **Pone suas** sic! Mihi ante vasta curvamine praesentem raptatur\nbarba sternere promissa in flexo.\n',
  profile_form: [
    {
      id: 432,
      label: 'How old are you',
      field_type: 'number',
      required: true,
    },
    {
      id: 434,
      label: 'How do you feel about privacy?',
      field_type: 'string',
      required: false,
    },
    {
      id: 435,
      label: 'Job Role',
      field_type: 'string',
      required: true,
    },
  ],
};

export function loadExercise() {
  return EXERCISES;
}
