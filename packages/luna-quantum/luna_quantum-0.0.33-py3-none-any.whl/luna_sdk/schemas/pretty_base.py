from datetime import datetime

from pydantic import BaseModel


class PrettyBase(BaseModel):
    def _pretty_print(self, data: dict, indent: int = 0) -> str:
        """Helper function to pretty print nested dictionaries in a readable yaml inspired format"""
        output = ""
        for key, value in data.items():
            output += "    " * indent + str(key) + ":"
            if isinstance(value, dict):
                if value == {}:
                    output += " {}\n"
                else:
                    output += "\n"
                    output += self._pretty_print(value, indent + 1)
            elif isinstance(value, datetime):
                output += f" {value.strftime('%Y-%m-%d %H:%M:%S (%Z)')}\n"
            else:
                output += f" {value}\n"
        return output

    def __str__(self):
        """Overwrite the default object string representation to use the custom pretty print console representation"""
        data = self.model_dump()

        return self._pretty_print(data)

    @property
    def head(self):
        """Print a truncated version of the pretty print console representation"""
        limit = 20

        def truncate(data, limit):
            if data is None:
                return None, False

            if isinstance(data, dict):
                d = {
                    k: truncate(v, limit)[0]
                    for i, (k, v) in enumerate(data.items())
                    if i < limit
                }
                return d, len(data) > limit
            elif isinstance(data, list):
                d = data[:limit]
                return d, len(data) > limit
            else:
                return data, False

        data = self.model_dump()

        data_truncated, is_truncated = truncate(data, limit)

        return self._pretty_print(data_truncated)
