#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @2024 AI. Inspur Inc.
#
# @author: sunxian <sunxian@inspur.com>
# @date: 2024/11/05
#


keys = ("title", "summary", "abstract", "text", "question", "answer", "code")

# data = {
#   "context": [{"role": "user", "content": xxx}, {"role": "assistant", "content": xxx}, ...],
#   "chosen": "xx",
#   "rejected": "xx"
# }

if not isinstance(messages, list) or not isinstance(messages[0], dict):
    raise ValueError("messages should be [{'role': 'xxx', 'content': 'xxx'}, ...]," + f" but got {messages}")

assert hasattr(tokenizer, "apply_chat_template"), "tokenizer should have apply_chat_template"
assert messages[-1]["role"] == "assistant", "messages[-1]['role'] should be 'assistant'"
assert messages[-2]["role"] == "user", "messages[-2]['role'] should be 'user'"
