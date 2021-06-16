from plover.formatting import Case, SPACE


def syllabic_caps(ctx, arg):
    """
    cmdline should be:
        caps: UPPERCASE
        lower: lowercase
        title: Title Case
        camel: titlecase, no space, initial lowercase
        snake: underscore_space
        reset_space: Space resets to ' '
        reset_case: Reset to normal case
        set_space:xy: Set space to xy
        reset: Reset to normal case, space resets to ' '
    """
    if arg != '':
        raise ValueError('syll_caps does not take arguments')
    action = ctx.copy_last_action()
    if action.case == Case.UPPER:
        action.case = None
    else:
        action.case = Case.UPPER
    return action
