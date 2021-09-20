import re
from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator, UserAttributeSimilarityValidator
from django.utils.translation import gettext as _, ngettext
from django.core.exceptions import (
    FieldDoesNotExist, ValidationError,
)
from difflib import SequenceMatcher

class CustomMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "Hasło jest za krótkie. Musi zawierać co najmniej %(min_length)d znak.",
                    "Hasło jest za krótkie. Musi zawierać co najmniej %(min_length)d znaków.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )


class CustomCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("Hasło jest zbyt powszechne."),
                code='password_too_common',
            )


class CustomNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("Hasło nie może być numeryczne."),
                code='password_entirely_numeric',
            )


class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    if verbose_name == 'username':
                        raise ValidationError(
                            _("Hasło jest zbyt podobne do nazwy użytkownika."),
                            code='password_too_similar',
                            params={'verbose_name': verbose_name},
                        )
                    elif verbose_name == 'first_name':
                        raise ValidationError(
                            _("Hasło jest zbyt podobne do imienia."),
                            code='password_too_similar',
                            params={'verbose_name': verbose_name},
                        )
                    elif verbose_name == 'last_name':
                        raise ValidationError(
                            _("Hasło jest zbyt podobne do nazwiska."),
                            code='password_too_similar',
                            params={'verbose_name': verbose_name},
                        )
                    else:
                        raise ValidationError(
                            _("Hasło jest zbyt podobne do %(verbose_name)s."),
                            code='password_too_similar',
                            params={'verbose_name': verbose_name},
                        )
