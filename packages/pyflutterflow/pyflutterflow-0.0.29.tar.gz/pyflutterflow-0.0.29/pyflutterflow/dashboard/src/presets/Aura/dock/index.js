export default {
    root: ({ props }) => ({
        class: [
            // Positioning
            'absolute z-1',
            {
                'left-0 bottom-0 w-full': props.position == 'bottom',
                'left-0 top-0 w-full': props.position == 'top',
                'left-0 top-0 h-full': props.position == 'left',
                'right-0 top-0 h-full': props.position == 'right'
            },

            // Flexbox & Alignment
            'flex justify-center items-center',

            // Interactivity
            'pointer-events-none'
        ]
    }),
    listContainer: {
        class: [
            // Flexbox
            'flex',

            // Shape & Border
            'rounded-md',

            // Color
            'bg-surface-0/10 dark:bg-surface-900/20 border border-surface-0/20',
            'backdrop-blur-sm',

            // Spacing
            'p-2',

            // Misc
            'pointer-events-auto'
        ]
    },
    list: ({ props }) => ({
        class: [
            // Flexbox & Alignment
            'flex items-center justify-center',
            {
                'flex-col': props.position == 'left' || props.position == 'right'
            },

            // List Style
            'm-0 p-0 list-none',

            // Shape
            'outline-none'
        ]
    }),
    item: ({ props, context, instance }) => ({
        class: [
            // Spacing & Shape
            'p-2 rounded-md',

            // Positioning & Hover States
            {
                'origin-bottom': props.position == 'bottom',
                'origin-top': props.position == 'top',
                'origin-left': props.position == 'left',
                'origin-right': props.position == 'right'
            },

            // Transitions & Transform
            'transition-all duration-200 ease-cubic-bezier-will-change-transform transform'
        ]
    }),
    itemLink: {
        class: [
            // Flexbox & Alignment
            'flex flex-col items-center justify-center',

            // Position
            'relative',

            // Size
            'w-16 h-16',

            // Misc
            'cursor-default overflow-hidden'
        ]
    }
};
