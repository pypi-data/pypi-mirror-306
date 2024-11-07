#!/usr/bin/env python3

from tiramisu import Option


class LipogramOption(Option):
    __slots__ = tuple()
    _type = 'lipogram'
    def __init__(self,
                 *args,
                 min_len=100,
                 **kwargs):
        # store extra parameters
        extra = {'_min_len': min_len}
        super().__init__(*args,
                         extra=extra,
                         **kwargs)

    def validate(self,
                 value):
        # first, valid that the value is a string
        if not isinstance(value, str):
            raise ValueError('invalid string')
        # and verify that there is any 'e' in the sentense
        if 'e' in value:
            raise ValueError('Perec wrote a book without any "e", you could not do it in a simple sentence?')

    def second_level_validation(self,
                                value,
                                warnings_only):
        # retrive parameter in extra
        min_len = self.impl_get_extra('_min_len')
        # verify the sentense length
        if len(value) < min_len:
            # raise message, in this case, warning and error message are different
            if warnings_only:
                msg = f'it would be better to have at least {min_len} characters in the sentence'
            else:
                msg = f'you must have at least {min_len} characters in the sentence'
            raise ValueError(msg)
