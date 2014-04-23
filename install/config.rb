# Example gollum config
# gollum ../wiki --config config.rb
#
# or run from source with
#
# bundle exec bin/gollum ../wiki/ --config config.rb

# Remove const to avoid
# warning: already initialized constant FORMAT_NAMES
#
# only remove if it's defined.
# constant Gollum::Page::FORMAT_NAMES not defined (NameError)
Gollum::Page.send :remove_const, :FORMAT_NAMES if defined? Gollum::Page::FORMAT_NAMES
Gollum::Page::FORMAT_NAMES = { :markdown  => "Markdown" }

Gollum::Hook.register(:post_commit, :hook_id) do |committer, sha1|
  system 'dtn-transmit.py nodeX && cat /tmp/nodeX.bundle.dtn > /tmp/tobesent'
end
