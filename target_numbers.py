def eval_to(nums, target, so_far = ""):
    strs, out, signs = [str(num) for num in nums], [], ["+", "-", ""]

    if len(nums) == 0:
        if eval(so_far) == target:
            return so_far
        return []
    for sign in signs:
        out += eval_to(strs[1:], so_far + sign + strs[0])
    return out

print eval_to([1,2,3], 6)
