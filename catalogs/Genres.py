from yamlable import yaml_info, YamlAble
import kiwilib

tag = 'Genre'


@yaml_info(yaml_tag_ns=tag)
class Genre(kiwilib.HierarchicalEnum, YamlAble): pass
@yaml_info(yaml_tag_ns=tag)
class GenreUndefined(Genre): pass  # Marks a Media instance as needing Genre(s) assigned. Used in DEFAULT_MEMBERS.
@yaml_info(yaml_tag_ns=tag)
class Fiction(Genre): pass
@yaml_info(yaml_tag_ns=tag)
class NonFiction(Genre): pass
@yaml_info(yaml_tag_ns=tag)
class Comedy(Genre): pass
@yaml_info(yaml_tag_ns=tag)
class Mystery(Genre): pass
@yaml_info(yaml_tag_ns=tag)
class Historical(Genre): pass
@yaml_info(yaml_tag_ns=tag)
class Drama(Genre): pass
@yaml_info(yaml_tag_ns=tag)
class SciFi(Fiction): pass
@yaml_info(yaml_tag_ns=tag)
class Fantasy(Fiction): pass
@yaml_info(yaml_tag_ns=tag)
class Educational(NonFiction): pass
@yaml_info(yaml_tag_ns=tag)
class SelfHelp(Educational): pass
@yaml_info(yaml_tag_ns=tag)
class Opinion(NonFiction): pass